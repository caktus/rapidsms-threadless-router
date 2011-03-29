from rapidsms.log.mixin import LoggerMixin
from rapidsms.utils.modules import try_import, get_class

from routerq.base import queue


__all__ = ('BackendBase',)


class BackendBase(object, LoggerMixin):

    @classmethod
    def find(cls, module_name):
        module = try_import(module_name)
        if module is None: return None
        return get_class(module, cls)

    def __init__ (self, router, name, **kwargs):
        self.router = router
        self.name = name

        self._config = kwargs
        if hasattr(self, "configure"):
            self.configure(**kwargs)

    def _logger_name(self): # pragma: no cover
        return "backend/%s" % self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<backend: %s>" % self.name
