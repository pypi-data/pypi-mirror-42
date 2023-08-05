# -*- coding: utf-8 -*-

import asyncio
import logging
import os
import re
import sys

import aiohttp
from sanic import Sanic
from sanic.exceptions import Forbidden
from sanic.response import json
from sanic.views import HTTPMethodView

from nadaprafazer.core import get_reddit_threads, get_joke
from nadaprafazer.exceptions import (BadCommand, BadTelegramAPICall,
                                     NoWebhookURL, TooLongMessage,
                                     BadSubreddit, BadTelegramToken)


HTTP_PORT = int(os.environ.get('HTTP_PORT', 8000))
DEFAULT_INVALID_TOKEN = 'a-invalid-token'
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', DEFAULT_INVALID_TOKEN)
TELEGRAM_URL = 'https://api.telegram.org/bot{}/'.format(TELEGRAM_TOKEN)
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

logger = logging.getLogger()

app = Sanic()


async def post_payload(url, payload):
    """Posts a payload to a given url.

    :param url: The destination of the payload.
    :param payload: An object that will be serialized into json.
    """

    async with aiohttp.ClientSession()as session:
        async with session.post(url, json=payload) as response:
            if response.status != 200:
                r = await response.text()
                if 'Bad Request: message is too long' in r:
                    raise TooLongMessage
                else:
                    raise BadTelegramAPICall(r)

    return True


async def set_webhook(webhook_url):
    """Sends a request to the telegram api registering this webhook.

    :param webhook_url: The url for the webhook. Note it that MUST be HTTPS.
      Your token - set the token using the ``TELEGRAM_TOKEN`` environment
      variable - will be added to the url so we can check if the request is
      from telegram. So, if `webhook_url` is ``https://bla.com/`` the
      registered webhook url at telegram will be
      ``https://bla.com/<your-token>``.
    """

    if not webhook_url.endswith('/'):
        webhook_url += '/'

    webhook_url += TELEGRAM_TOKEN
    payload = {'url': webhook_url}
    url = TELEGRAM_URL + 'setWebhook'

    await post_payload(url, payload)


async def webhook_is_set():
    """Indicates if the webhook for the bot is configured or not."""

    url = TELEGRAM_URL + 'getWebhookInfo'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            r = await response.json()

    try:
        r = bool(r['result']['url'])
    except KeyError:
        # key error happens when we send a bad token
        raise BadTelegramToken

    return r


async def maybe_set_webhook():
    """Sets the webhook for the bot if it is not configured yet.

    When setting the webhook, uses the ``WEBHOOK_URL`` environment variable
    to get its value.
    """

    has_webhook = await webhook_is_set()
    if has_webhook:
        return False

    if not WEBHOOK_URL:
        raise NoWebhookURL

    await set_webhook(WEBHOOK_URL)


class TelegramWebhookHandler(HTTPMethodView):
    """Handles incomming webhooks from telegram."""

    def check_token(self, token):
        """Checks if the a given token the right one. If the token is invalid
         raises a :class:`~sanic.exceptions.Forbidden` error

        :param token: A token sent by telegram - usually as part of the url
        """

        if token != TELEGRAM_TOKEN or TELEGRAM_TOKEN == DEFAULT_INVALID_TOKEN:
            raise Forbidden('Bad api token')

        return True

    async def send_message(self, payload):
        """Sends a given payload to the telegram api

        :param payload: A object that will be serialized into a json
          and sent to the telegram api.
        """

        url = '{}sendMessage'.format(TELEGRAM_URL)

        await post_payload(url, payload)
        return True

    def get(self, request, token=None):
        """This is kinda heath check."""
        out = 'I\'m alive!'

        return json({'message': out})

    def post(self, request, token):
        """Handles the post request from telegram.
        """
        # you should do something else here...
        self.check_token(token)


class HotRedditBotHandler(TelegramWebhookHandler):
    """Handles webhooks for the HotRedditBot. The HotRedditBot, when
    recieves a `/hotties subreddit;other;other` command, uses
    :func:`~nadaprafazer.core.get_reddit_threads` to get the most
    upvoted threads from the subreddits provided or from a random one and
    send the results back to the chat on telegram.
    """

    NORMAL_FACE = '(o_o)'
    IDONTKNOW_FACE = '¯\\_(o_o)_/¯'
    CONFUSED_FACE = '(o_O)'
    SCARED_FACE = '(O_O)'
    GREETING_FACE = '(o_o)ノ'
    EXPLAINING_FACE = '&lt(o _o)y-~~'

    THREADS_LIMIT = 25

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._commands = {'/hotties': self.handle_hotties_command,
                          '/start': self.handle_start_command,
                          '/help': self.handle_help_command,
                          '/joke': self.handle_joke_command}

        # alias
        self._commands['/NadaPraFazer'] = self._commands['/hotties']

    def _escape_chars(self, entry):
        for k, v in entry.items():
            try:
                entry[k] = v.replace('&', '&amp').replace('<', '&lt').replace(
                    '>', '&gt')
            except AttributeError:
                # something that is not a string...
                pass
        return entry

    async def send_message(self, payload):
        """Sends a message and if the message is too longe sends a
        message informing about it.

        :param payload: An object that will be serialized into a json
          and sent to the telegram api.
        """
        try:
            r = await super().send_message(payload)
        except TooLongMessage:
            msg = '{}\n\nToo many threads. Lower the limit.'.format(
                self.SCARED_FACE)
            payload = {'chat_id': payload['chat_id'],
                       'text': msg}

            await super().send_message(payload)

            r = False

        return r

    def format_entry(self, entry):
        """Formats a thread entry using markdown.

        :param entry: A dictionary with info about a reddit thread.
        """

        template = '''
<strong>{title}</strong>
<a href="{thread_link}">thread</a>
<a href="{comments_link}">comments</a>
votes: {votes}
subreddit: {subreddit}'''

        return template.format(**self._escape_chars(entry))

    def check_text(self, text):
        """Check if the text sent by the user is valid command.
        """
        # returns cmd, args_str
        splitted = text.split(' ', 1)

        if not splitted[0] in self._commands:
            raise BadCommand

        if len(splitted) == 1:
            splitted.append('')

        return splitted

    def parse_hotties_command_args(self, args):
        """Here we get a string with the arguments of the /hotties command,
        something like this: 'python;emacs t100' and we parse it
        returning args, and kwrags to
        :func:`~nadaprafazer.core.get_reddit_threads`"""

        fargs, fkwargs = [], {}

        patterns = ((re.compile(r't(\d+)'), 'votes_threshold'),
                    (re.compile(r'l(\d+)'), 'threads_limit'))

        for pattern, key in patterns:
            match = pattern.search(args)

            if match:
                fkwargs[key] = int(match.groups()[0])
                args = pattern.sub('', args)

        if not fkwargs.get('threads_limit'):
            fkwargs['threads_limit'] = self.THREADS_LIMIT

        args = [a.strip() for a in args.split() if a.strip()]
        if len(args) > 1:
            raise BadCommand(' '.join(args[1:]))

        elif len(args) == 0:
            fargs = []
        else:
            arg = args[0]
            fargs = [a.strip() for a in arg.split(';')]

        return fargs, fkwargs

    async def handle_hotties_command(self, chat_id, cmd_args):
        """Handles the `/hotties` command.

        Gets a list from the hottest threads in reddit and send it
        to a telegram chat.

        :param chat_id: The id of the telegram chat
        :param cmd_args: A string with the command arguments sent by the user.
        """

        try:
            args, kwargs = self.parse_hotties_command_args(cmd_args)
        except BadCommand as e:
            msg = "{}\n\nWhat do you mean with '{}'?".format(
                self.CONFUSED_FACE, str(e))

            payload = {'chat_id': chat_id,
                       'text': msg}
            await self.send_message(payload)
            return False

        try:
            entires = await get_reddit_threads(*args, **kwargs)
        except BadSubreddit as e:
            msg = "{}\n\n{}".format(self.NORMAL_FACE, str(e))

            payload = {'chat_id': chat_id,
                       'text': msg}
            await self.send_message(payload)
            return False

        if not entires:
            text = '{} \n\n \
No hotties here. Be less picky. Lower the votes threshold.'.format(
                self.NORMAL_FACE)
        else:
            text = '\n'.join([self.format_entry(e) for e in entires])

        payload = {'chat_id': chat_id,
                   'text': text,
                   'parse_mode': 'html',
                   'disable_web_page_preview': True}

        await self.send_message(payload)
        return True

    async def handle_start_command(self, chat_id, cmd_args):
        msg = """{}

Hi! I'm the <strong>HotRedditBot</strong>.

I can show you the hottest reddit threads. Try /hotties for a start.
For a complete help use /help""".format(self.GREETING_FACE)
        payload = {'chat_id': chat_id,
                   'text': msg,
                   'parse_mode': 'html'}

        await self.send_message(payload)

    async def handle_help_command(self, chat_id, cmd_args):
        # this ugly stuff here is that I don't wanna have \n
        # here so it looks better on telegram screen but I also don't
        # want huge lines on my screen, so...
        paras = ['{}'.format(self.EXPLAINING_FACE)]

        msg = """Use the command /hotties - or its alias /NadaPraFazer - to get
the hottest reddit threads. With no arguments I'll show you
the hotties from the reddit front page. You can specify subreddits using:
""".replace('\n', ' ')
        paras.append(msg)
        paras.append("""/hotties askreddit
/hotties worldnews;brasil
""")

        msg = '''By default, only threads with 5k+ upvotes are shown. To
change this threshold use:
'''.replace('\n', ' ')

        paras.append(msg)

        paras.append("""/hotties python;emacs t100

<b>t100</b> will change the threshould to 100 upvotes.

I will show you at most 25 threads. To change this, use:

/hotties l10

<b>l10</b> will change the limit to 10 threads.

The /joke command will show you a random joke from r/jokes.

And you can always use /help for this message.
        """)

        payload = {'chat_id': chat_id,
                   'text': '\n\n'.join(paras),
                   'parse_mode': 'html'}

        await self.send_message(payload)

    async def handle_joke_command(self, chat_id, cmd_args):
        template = '''
<b>{title}</b>

{body}
<a href="{thread_link}">thread</a>
'''
        joke = await get_joke()

        txt = template.format(**joke)

        payload = {'chat_id': chat_id,
                   'text': txt,
                   'disable_web_page_preview': True,
                   'parse_mode': 'html'}

        await self.send_message(payload)

    async def post(self, request, token):

        super().post(request, token)

        payload = request.json

        try:
            chat_id = payload['message']['chat']['id']
        except KeyError:
            logger.error('Bad payload: {}'.format(str(payload)))
            return json({'status': 'fail'})

        try:
            cmd, args = self.check_text(payload['message']['text'])
        except (BadCommand, KeyError):
            # KeyError is for messages without text
            msg = """{}\n\nTry /help""".format(self.IDONTKNOW_FACE)
            payload = {'chat_id': chat_id,
                       'text': msg}

            asyncio.ensure_future(self.send_message(payload))
        else:
            parse_command = self._commands[cmd]
            asyncio.ensure_future(parse_command(chat_id, args))

        return json({'status': 'ok'})


app.add_route(HotRedditBotHandler.as_view(), '/<token>', methods=['POST'])
app.add_route(HotRedditBotHandler.as_view(), '/', methods=['GET'])


def main():  # pragma no cover

    if TELEGRAM_TOKEN == DEFAULT_INVALID_TOKEN:
        print('You need to set the TELEGRAM_TOKEN environment variable')
        sys.exit(1)

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(maybe_set_webhook())
    except NoWebhookURL:
        print('You need to set the WEBHOOK_URL environment variable.')
        sys.exit(1)
    except BadTelegramToken:
        print('Seems your TELEGRAM_TOKEN isn\'t right.')
        sys.exit(1)
    else:
        app.run('0.0.0.0', port=HTTP_PORT)


if __name__ == '__main__':  # pragma no cover
    main()
