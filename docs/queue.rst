Asynchronous Task Queues
========================

``threadless_router`` allows inbound messages to be easily passed off to an
asynchronous task queue, such as `Celery <http://celeryproject.org/>`_.  Task
queues allow message processing to be handled outside of the HTTP
request/response cycle.

django-celery
-------------

A celery handler is bundled for example.

* Install ``djcelery`` with pip::

    pip install django-celery==2.2.4

* Add ``djcelery`` and ``threadless_router.celery`` apps to ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        # ...
        "djcelery",
        "threadless_router.celery",
        # ...
    ]

* Point backend handler(s) to celery task::

    INSTALLED_BACKENDS = {
        # ...
        "simple-http": {
            "ENGINE": '...'.
            "HANDLER": "threadless_router.celery.handler", # <-----
            "outgoing_url": '...',
        },
        # ...
    }

* Start ``celeryd`` in separate shell::

    $ ./manage.py celeryd

* Now all inbound messages to the "simple-http" backend will respond out-of-band via a celery task.
