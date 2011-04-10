import logging

from django.conf import settings

from rapidsms.tests.scripted import TestScript as LegacyTestScript
from rapidsms.tests.harness import MockBackend

from threadless_router.router import Router


class TestScript(LegacyTestScript):

    def setUp (self):
        backends = {'mockbackend': {"ENGINE": MockBackend}}
        self.router = Router(apps=self.apps, backends=backends)
        self.router.join = lambda: None
        self._init_log(logging.DEBUG)
        self.backend = self.router.backends["mockbackend"]

    def sendMessage(self, num, txt, date=None):
        self.router.debug('sending {0} to {1}'.format(txt, num))
        return super(TestScript, self).sendMessage(num, txt, date)

    def receiveMessage(self):
        msg = super(TestScript, self).receiveMessage()
        self.router.debug(msg)
        return msg

    def startRouter(self):
        pass

    def stopRouter(self):
        pass
