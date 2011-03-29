from rapidsms.conf import settings
from rapidsms.router import Router as LegacyRouter


class Router(LegacyRouter):
    """ RapidSMS router with the threading and Queue parts removed """

    def __init__(self):
        super(Router, self).__init__()
        self.start()

    def start(self):
        self.info("starting router")
        for name in settings.INSTALLED_APPS:
            self.add_app(name)
        for name, conf in settings.INSTALLED_BACKENDS.items():
            self.add_backend(name, conf.get("ENGINE"), conf)
        self._start_all_apps()
        self.running = True

    def stop(self, graceful=False):
        self.info("stopping router")
        self._stop_all_apps()
        self.running = False

    def incoming(self, msg):
        # disable IncomingMessage.flush_responses
        msg.flush_responses = lambda: None
        # process incoming phases as usual
        super(Router, self).incoming(msg)
        # handle message responses from within router
        for response in msg.responses:
            self.outgoing(response)

    def outgoing(self, msg):
        # disable OutgoingMessage.send_now
        msg.send_now = lambda: None
        # process outgoing phase as usual
        super(Router, self).outgoing(msg)
        # send message from within router
        self.backends[msg.connection.backend.name].send(msg)
