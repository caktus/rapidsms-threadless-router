Using rapidsms-threadless-router with Kannel
============================================

Given the fact that ``threadless_router`` uses a Django view to handle
incoming messages, instead of its own HTTP server like RapidSMS's Kannel
backend does, ``threadless_router`` fits perfectly with the Kannel model of
sending and receiving all messages over HTTP in a simple, scalable way.

Kannel Configuration
--------------------

Kannel configuration can be a non-trivial task, depending on what gateways
you're using.  Complete details can be found in the Kannel documentation
itself.

To configure Kannel to connect to a RapidSMS project that uses 
``threadless_router``, you need to add a few things to your Kannel
configuration (usually ``/etc/kannel/kannel.conf``).

* Add a ``sendsms-user`` for RapidSMS to connect as::

    group = sendsms-user
    username = rapidsms
    password = change-me
    user-deny-ip = "*.*.*.*"
    user-allow-ip = "127.0.0.1;"

* Add an ``sms-service`` entry to handle inbound messages for RapidSMS::

    group = sms-service
    keyword = default
    # don't send a reply here (it'll come through sendsms):
    max-messages = 0
    get-url = http://127.0.0.1:8000/backend/my-kannel-backend/?id=%p&text=%a&charset=%C&coding=%c

``threadless_router`` Configuration
-----------------------------------

The ``kannel`` backend provides an implementation of the ``http`` backend for
integrating with Kannel.  To enable the `kannel` backend on an existing
project, complete the following steps:

* Add `kannel` app to ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        # ...
        "threadless_router.backends.kannel",
        # ...
    ]

* Add `my-kannel-backend` to ``INSTALLED_BACKENDS``::

    INSTALLED_BACKENDS = {
        # ...
        "my-kannel-backend": {
            "ENGINE":  "threadless_router.backends.kannel.outgoing",
            "sendsms_url": "http://127.0.0.1:13013/cgi-bin/sendsms",
            "sendsms_params": {"smsc": "usb0-modem", # if you have more than one
                               "from": "1234", # may not be set automatically by SMSC
                               "username": "rapidsms",
                               "password": "change-me"},
            "coding": 0,
            "charset": "ascii",
            "encode_errors": "ignore", # strip out unknown (unicode) characters
        },
        # ...
    }

* Add ``kannel`` urls::

    urlpatterns = patterns('',
        # ...
        (r'^backend/', include('threadless_router.backends.kannel.urls')),
        # ...
    )

* Now incoming requests to /backend/my-kannel-backend/ will be handled by the
newly configured Kannel backend.
