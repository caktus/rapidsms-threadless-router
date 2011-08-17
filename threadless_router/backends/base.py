from rapidsms.backends.base import BackendBase as RapidBackendBase


class BackendBase(RapidBackendBase):
    """
    Backend that overrides the default RapidSMS backend to keep threads
    from starting.
    """

    def start(self):
        """ Override BackendBase.start(), which never returns """
        self._running = True
