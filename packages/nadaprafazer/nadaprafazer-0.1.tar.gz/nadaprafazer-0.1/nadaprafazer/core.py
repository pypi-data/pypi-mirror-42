# -*- coding: utf-8 -*-
"""This module contains stuff related to download and parsing of
subreddit pages.
"""

import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import partial
import os
import random

import aiohttp
import bs4

from nadaprafazer.cache import cache
from nadaprafazer.exceptions import BadSubreddit, BadPage


POOL = ProcessPoolExecutor()
REDDIT_URL = 'https://old.reddit.com'
VOTES_THRESHOLD = 5000
CACHE_TIME = int(os.environ.get('CACHE_TIME', 300))


async def _fetch(session, url):
    """Fetchs a url and returns the body of the response

    :param session: An aiohttp session we use to request the page.
    :param url: The url you want to fetch.
    """
    async with session.get(url) as response:
        if response.status == 404:
            raise BadSubreddit
        content = await response.text()

    return content


def _fix_url(url):
    if not url.startswith('http'):
        url = REDDIT_URL + url

    return url


def _parse_vote(vote_str):
    """Parses the number of votes in a reddit thread.

    If it ends with 'k', the number is multiplied by 1000, if it ends with
    'm', the number is multiplied by 10000, otherwise we consider it an int.

    :param vote_str: The string that is in the html representing the
      number of votes.
    """

    if vote_str[-1].lower() == 'k':
        vote = int(float(vote_str[:-1]) * 1000)
    elif vote_str[-1].lower() == 'm':
        vote = int(float(vote_str[:-1]) * 10000)
    else:
        try:
            vote = int(vote_str)
        except ValueError:
            # When we have zero votes, instead of a 0 we have a silly dot `•`
            vote = 0
    return vote


def _is_search(soup):
    """Checks if a soup is from a reddit search page.

    :param soup: A bs4 parsed html.
    """

    return bool(soup.find(class_='searchpane'))


def parse_joke(content):
    soup = bs4.BeautifulSoup(content, 'html.parser')
    entry = soup.find(class_='thing')
    title = entry.find('a', class_='title').text
    body = entry.find(class_='usertext-body').text.strip(' \n')

    return {'title': title, 'body': body}


def parse_thread_list(content, votes_threshold=0):
    """Parses the html from a subreddit page - or main page - to extract
    relevant information.

    :param content: The html returned by a subreddit page.
    :param votes_threshold: If an entry's votes do not match this threshold
      the entry will not be returned. If no threshold all entries will be
      returned.
    """
    soup = bs4.BeautifulSoup(content, 'html.parser')

    if _is_search(soup):
        # When we request a subreddit that doesn't exist we get a search page.
        # We only know how to parse main reddit page and subreddits pages.
        raise BadPage

    subreddit = soup.find(class_='redditname')
    subreddit = '' if not subreddit else subreddit.text
    parsed_entries = []

    for html_entry in soup.find_all(class_='thing'):
        # we do it here so if we don't met the threshold we give up on the
        # entry now
        votes = _parse_vote(html_entry.find(class_='score unvoted').text)
        if votes_threshold and votes < votes_threshold:
            continue
        try:
            comments_link = _fix_url(
                html_entry.find('a', class_='comments')['href'])
        except TypeError:
            # promoted stuff has no comment link and we don't want
            # propaganda - yes, propaganda! - here.
            continue

        title = html_entry.find('a', class_='title').text
        link = _fix_url(html_entry.find('a', class_='title')['href'])

        entry_subreddit = html_entry.find('a', class_='subreddit')

        subreddit = subreddit if not entry_subreddit else entry_subreddit.text
        subreddit = subreddit.strip('r/')
        entry = {'title': title,
                 'subreddit': subreddit,
                 'votes': votes,
                 'thread_link': link,
                 'comments_link': comments_link}

        parsed_entries.append(entry)

    return parsed_entries


async def _run_in_process_pool(fn, loop=None):
    """Runs a function in a process pool and returns its result.

    :param fn: A function to run in the child process.
    :param loop: The ioloop used. If None, uses ``asyncio.get_event_loop()``.
    """

    loop = loop or asyncio.get_event_loop()
    r = await loop.run_in_executor(POOL, fn)
    return r


async def _fetch_and_parse(session, url, votes_threshold=VOTES_THRESHOLD,
                           loop=None):
    """Fetches an url and does the parsing of its contents
    in a process pool. Returns a list of dictionaries with relevant info.

    :param session: An aiohttp session we use to request the page.
    :param url: A reddit url you want to extract info.
    :param votes_threshold: If an entry's votes do not match this threshold
      the entry will not be returned. If no threshold all entries will be
      returned.
    :param loop: The ioloop used. If None, uses ``asyncio.get_event_loop()``.
    """

    content = await _fetch(session, url)
    parse_fn = partial(parse_thread_list, content, votes_threshold)

    r = await _run_in_process_pool(parse_fn, loop=loop)

    return r


@cache(CACHE_TIME)
async def get_threads_from(subreddit, sort=True,
                           votes_threshold=VOTES_THRESHOLD):
    """Returns a list of threads with more upvotes on a subreddit.

    :param subreddit: The name of a subreddit you want to get information.
    :param sort: Should we return the threads sorted by votes?
    :param votes_threshold: If an entry's votes do not match this threshold
      the entry will not be returned. If no threshold all entries will be
      returned.
    """

    if subreddit:
        url = REDDIT_URL + '/r/' + subreddit
    else:
        url = REDDIT_URL

    async with aiohttp.ClientSession() as session:
        try:
            r = await _fetch_and_parse(session, url, votes_threshold)
        except BadPage:
            # When the parser doesn't know what to do with a page that
            # means the subreddit we are looking for does not exist.
            msg = 'The subreddit "{}" does not seem to exist.'.format(
                subreddit)
            raise BadSubreddit(msg)

    if sort:
        r = sorted(r, key=lambda t: t['votes'],  # pragma no branch
                   reverse=True)

    return r


async def _gather_results(tasks):
    await asyncio.gather(*tasks)
    result = []
    for t in tasks:
        result += t.result()

    return result


async def get_reddit_threads(*subreddits, votes_threshold=VOTES_THRESHOLD,
                             threads_limit=None):
    """Returns a list of most upvoted threads on reddit.

    :param subreddits: A list of subreddit names you want to get info from. If
      no subreddits, will get info from a random one.
    :param votes_threshold: If an entry's votes do not match this threshold
      the entry will not be returned. If no threshold all entries will be
      returned.
    """

    subreddits = subreddits or ['']

    tasks = [asyncio.ensure_future(
        get_threads_from(s, sort=False, votes_threshold=votes_threshold))
        for s in subreddits]

    r = await _gather_results(tasks)

    sorted_threads = sorted(r, key=lambda t: t['votes'], reverse=True)
    if threads_limit:
        sorted_threads = sorted_threads[:threads_limit]

    return sorted_threads


@cache(CACHE_TIME)
async def _get_joke_from_url(url):
    async with aiohttp.ClientSession() as session:
        joke_html = await _fetch(session, url)

    fn = partial(parse_joke, joke_html)

    joke = await _run_in_process_pool(fn)
    return joke


async def get_joke():
    """Returns a random joke from r/jokes."""

    subreddit = 'jokes'

    entries = await get_threads_from(subreddit, votes_threshold=0,
                                     sort=False)
    entry = random.choice(entries)
    thread_link = entry['thread_link']

    joke = await _get_joke_from_url(thread_link)
    joke['thread_link'] = thread_link

    return joke
