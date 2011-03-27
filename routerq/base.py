import datetime

from rapidsms.models import Connection, Backend

from routerq.router import Router
from routerq.messages import IncomingMessage


def queue(identity, body, backend):
    be, _ = Backend.objects.get_or_create(name=backend.name)
    connection, _ = be.connection_set.get_or_create(identity=identity)
    message = IncomingMessage(connection, body, datetime.datetime.now())
    
    router = Router()
    response = router.incoming(message)
    print response
