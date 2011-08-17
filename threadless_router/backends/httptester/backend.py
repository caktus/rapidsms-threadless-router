from threadless_router.backends.base import BackendBase

from threadless_router.backends.httptester.storage import store_message


class HttpTesterCacheBackend(BackendBase):
    """ Simple backend that stores messages in a cache """

    def send(self, msg):
        store_message('out', msg.connection.identity, msg.text)

    def start(self):
        """ Override BackendBase.start(), which never returns """
        self._running = True
