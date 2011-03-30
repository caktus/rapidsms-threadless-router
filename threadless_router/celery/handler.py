from threadless_router.celery.tasks import IncomingTask


def incoming(backend_name, identity, text):
    IncomingTask.delay(backend_name, identity, text)
