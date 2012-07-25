import datetime

from rapidsms.models import Backend
from rapidsms.messages import IncomingMessage

from threadless_router.router import Router

from celery.task import Task
from celery.registry import tasks


class IncomingTask(Task):
    def run(self, backend_name, identity, text):
        backend, _ = Backend.objects.get_or_create(name=backend_name)
        connection, _ = backend.connection_set.get_or_create(identity=identity)
        message = IncomingMessage(connection, text, datetime.datetime.now())
        router = Router()
        response = router.incoming(message)


tasks.register(IncomingTask)
