""" Store and get messages from cache """

from django.core.cache import cache

from threadless_router.base import queue


CACHE_KEY = 'http-tester-cache'


def get_messages():
    return cache.get(CACHE_KEY, [])


def store_message(direction, identity, text):
    messages = get_messages()
    data = {"identity": identity, "direction": direction, "text": text}
    messages.append(data)
    cache.set(CACHE_KEY, messages)


def store_and_queue(identity, text):
    store_message('in', identity, text)
    queue('httptester-cache', identity, text)
