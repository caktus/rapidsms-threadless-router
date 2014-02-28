import datetime

from rapidsms.models import Backend
from rapidsms.messages import IncomingMessage

from threadless_router.router import Router
from threadless_router.base import incoming

from celery.task import Task
from celery.registry import tasks


class IncomingTask(Task):
    def run(self, backend_name, identity, text):
        incoming(backend_name, identity, text)


tasks.register(IncomingTask)
