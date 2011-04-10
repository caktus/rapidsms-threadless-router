from rapidsms.tests.harness import MockBackend

from threadless_router.router import Router


class SimpleRouterMixin(object):

    def setUp(self):
        super(SimpleRouterMixin, self).setUp()
        backends = {'mockbackend': {"ENGINE": MockBackend}}
        self.router = Router(backends=backends)
