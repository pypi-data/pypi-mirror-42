# -*- coding: utf-8 -*-


class BadPage(Exception):
    pass


class BadSubreddit(Exception):
    pass


class BadCommand(Exception):
    pass


class BadTelegramAPICall(Exception):
    pass


class NoWebhookURL(Exception):
    pass


class TooLongMessage(Exception):
    pass


class BadTelegramToken(Exception):
    pass
