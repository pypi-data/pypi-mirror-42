# -*- coding: utf-8 -*-

import argparse
import asyncio
import sys

from nadaprafazer.core import get_reddit_threads, VOTES_THRESHOLD, get_joke
from nadaprafazer.exceptions import BadSubreddit


async def show_threads(*subreddits, votes_threshold=VOTES_THRESHOLD):
    """Shows a list of information about reddit threads.

    :param subreddits: A list of subreddit names you want to get info from. If
      no subreddits, will get info from a random one.
    """

    head = '\nThe hotest threads for {}\n'.format(
        ', '.join(subreddits or ['reddit']))
    head += '=' * (len(head) - 2) + '\n'
    print(head)
    try:
        threads = await get_reddit_threads(*subreddits,
                                           votes_threshold=votes_threshold)
    except BadSubreddit as e:
        print(str(e))
        sys.exit(1)

    for t in threads:
        print('- {}'.format(t['title']))
        print('  votes: {}'.format(t['votes']))
        print('  subreddit: {}'.format(t['subreddit']))
        print('  thread link: {}'.format(t['thread_link']))
        print('  comments link: {}'.format(t['comments_link']))
        print('-' * 60)
        print('')


async def show_joke():
    joke = await get_joke()
    print(joke['title'])
    print('=' * len(joke['title']))
    print(joke['body'])


def main():

    parser = argparse.ArgumentParser(
        description='Shows the hotest threads from reddit')

    subhelp = '\
A list of reddits separated by semicolon. Yeah, I know... \
but it is a requirement. If not subreddits, a random subreddit will be \
chosen.'
    parser.add_argument('subreddits', nargs='?', help=subhelp)

    thelp = 'The threshold for votes. Threads with less upvotes than that \
will not be shown.'
    parser.add_argument('-t', default=VOTES_THRESHOLD, type=int,
                        help=thelp)

    parser.add_argument('--joke', action='store_true')

    args = parser.parse_args()
    joke = args.joke
    loop = asyncio.get_event_loop()
    if joke:
        loop.run_until_complete(show_joke())
    else:
        subreddits = args.subreddits
        subreddits = subreddits.split(';') if subreddits else []
        threshold = args.t
        loop.run_until_complete(
            show_threads(*subreddits, votes_threshold=threshold))


if __name__ == '__main__':
    main()
