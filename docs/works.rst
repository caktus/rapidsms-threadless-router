Differences to RapidSMS' Router
===============================

The legacy RapidSMS ``router`` is a globally instantiated object that routes
incoming messages through each RapidSMS app and sends outgoing messages via
installed backends.  The *run_router* management command starts the router
process and creates individual threads for each backend defined in the settings
module.

In comparison, ``threadless_router`` handles all inbound and outbound backend
communication from within the main HTTP thread.  Each request creates a new
``router`` instance and no seperate process or thread is created.
``threadless_router`` backends all use a single point of entry into the routing
functionality via ``incoming``::

    def incoming(backend_name, identity, text):
        backend, _ = Backend.objects.get_or_create(name=backend_name)
        connection, _ = backend.connection_set.get_or_create(identity=identity)
        message = IncomingMessage(connection, text, datetime.datetime.now())
        router = Router()
        response = router.incoming(message)

Given a backend name, phone number, and messsage, ``incoming`` creates a new
``router`` instance and triggers the incoming phases.  Here's a very simple
Django view that extracts phone and message variables from an HTTP POST and
passes it off to ``incoming``::

    from threadless_router.base import incoming

    def new_message(request, backend_name):
        incoming(backend_name, request.POST['phone'], request.POST['message'])
        return HttpResponse('OK')

It's important to note here that ``backend_name`` is passed in as part of the
request.  This is how inbound messages are paired with each defined backend.
For example, you could create two entry points into the ``httptester`` app::

    INSTALLED_BACKENDS = {
        "httptester-public": {
            "ENGINE": "threadless_router.backends.httptester.backend",
        },
        "httptester-private": {
            "ENGINE": "threadless_router.backends.httptester.backend",
        },
    }

The chosen backend is determined by the URL::

    >>> import urllib
    >>> import urllib2
    >>> data = urllib.urlencode({'identity': '1112223333', 'text': 'echo hello'})
    >>> urllib2.urlopen('http://localhost:8000/httptester/httptester-public/', data).read()
    'OK'
    >>> urllib2.urlopen('http://localhost:8000/httptester/httptester-private/', data).read()
    'OK'
