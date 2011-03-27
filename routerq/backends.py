from rapidsms.log.mixin import LoggerMixin

from routerq.base import queue


class BackendBase(object, LoggerMixin):

    def _logger_name(self): # pragma: no cover
        return "backend/%s" % self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<backend: %s>" % self.name

    def message(self, identity, text):
        queue(identity, text, self)
