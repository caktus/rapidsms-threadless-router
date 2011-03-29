import datetime

from rapidsms.models import Connection, Backend

from threadless_router.router import Router
from rapidsms.messages import IncomingMessage


__all__ = ('queue',)


def queue(identity, text, backend_name):
    backend, _ = Backend.objects.get_or_create(name=backend_name)
    connection, _ = backend.connection_set.get_or_create(identity=identity)
    message = IncomingMessage(connection, text, datetime.datetime.now())
    router = Router()
    response = router.incoming(message)
