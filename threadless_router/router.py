import copy
import datetime
import inspect

from rapidsms.conf import settings
from rapidsms.router import Router as LegacyRouter
from rapidsms.backends.base import BackendBase
from rapidsms.apps.base import AppBase


class Router(LegacyRouter):
    """ RapidSMS router with the threading and Queue parts removed """

    def __init__(self, apps=None, backends=None):
        super(Router, self).__init__()
        apps = apps or settings.INSTALLED_APPS
        backends = backends or settings.INSTALLED_BACKENDS
        self.start(apps, backends)

    def start(self, apps, backends):
        self.info("starting router")
        for name in apps:
            try:
                self.add_app(name)
            except Exception as e:
                self.exception(e)
        for name, conf in backends.iteritems():
            parsed_conf = copy.copy(conf)
            engine = parsed_conf.pop('ENGINE')
            self.add_backend(name, engine, parsed_conf)
        self.info('backends: {0}'.format(self.backends.keys()))
        self.info('apps: {0}'.format(self.apps))
        self._start_all_apps()
        self._start_all_backends()
        self.running = True

    def stop(self, graceful=False):
        self.info("stopping router")
        self._stop_all_apps()
        self._stop_all_backends()
        self.running = False

    def add_backend(self, name, module_name, config=None):
        """
        Find the backend named *module_name*, instantiate it, and add it
        to the dict of backends to be polled for incoming messages, once
        the router is started. Return the backend instance.
        """
        if not inspect.isclass(module_name):
            try:
                cls = BackendBase.find(module_name)
            except AttributeError:
                cls = None
        elif issubclass(module_name, BackendBase):
            cls = module_name
        if not cls:
            return None
        config = self._clean_backend_config(config or {})
        backend = cls(self, name, **config)
        self.backends[name] = backend
        return backend

    def add_app(self, module_name):
        """
        Find the app named *module_name*, instantiate it, and add it to
        the list of apps to be notified of incoming messages. Return the
        app instance.
        """
        if not inspect.isclass(module_name):
            try:
                cls = AppBase.find(module_name)
            except AttributeError:
                cls = None
        elif issubclass(module_name, AppBase):
            cls = module_name
        if not cls:
            return None
        app = cls(self)
        self.apps.append(app)
        return app

    def _start_all_backends(self):
        for backend in self.backends.values():
            backend.start()

    def _stop_all_backends(self):
        for backend in self.backends.values():
            backend.stop()

    def incoming_message(self, msg):
        """ Support legacy usage """
        return self.incoming(msg)

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
        self.sent = self.backends[msg.connection.backend.name].send(msg)
        msg.sent = self.sent
        return self.sent
