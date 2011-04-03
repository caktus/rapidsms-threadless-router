import datetime

from rapidsms.conf import settings
from rapidsms.messages import IncomingMessage
from rapidsms.models import Connection, Backend
from rapidsms.utils.modules import try_import

from threadless_router.router import Router


__all__ = ('incoming',)


def incoming(backend_name, identity, text):
    backend = settings.INSTALLED_BACKENDS.get(backend_name, {})
    if "HANDLER" in backend:
        module = try_import(backend['HANDLER'])
        if module:
            module.incoming(backend_name, identity, text)
    else:
        backend, _ = Backend.objects.get_or_create(name=backend_name)
        connection, _ = backend.connection_set.get_or_create(identity=identity)
        message = IncomingMessage(connection, text, datetime.datetime.now())
        router = Router()
        response = router.incoming(message)
