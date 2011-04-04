rapidsms-threadless-router
==========================

A `RapidSMS <https://github.com/rapidsms/rapidsms>`_ router implementation that
removes the threading functionality from the legacy Router class.

httptester
----------

``httptester`` overrides key components in the legacy ``httptester`` app
to provide identical functionality.  Django's cache backend is used as dummy
storage.

**httptester Setup**

* Add `httptester` to ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        # ...
        "threadless_router.backends.httptester",
        # ...
    ]

* Add `httptester` to ``INSTALLED_BACKENDS``::

    INSTALLED_BACKENDS = {
        # ...
        "httptester": {
            "ENGINE": "threadless_router.backends.httptester.backend",
        },
        # ...
    }

* Add ``httptester`` urls::

    urlpatterns = patterns('',
        # ...
        url(r'^httptester/$',
            'threadless_router.backends.httptester.views.generate_identity',
            {'backend_name': 'httptester'}, name='httptester-index'),
        (r'^httptester/', include('threadless_router.backends.httptester.urls')),
        # ...
    )

* Update ``RAPIDSMS_TABS`` to reference new view::

    RAPIDSMS_TABS = [
        # ...
        ("httptester-index", "Message Tester"),
        # ...
    ]

HTTP backend
------------

The ``http`` backend provides the foundation for building http-powered
services.  Built on top of Django 1.3's class-based generic views, the
``BaseHttpBackendView`` allows for easy extension and customization.  A simple
``SimpleHttpBackendView`` is bundled as a quick start example.

**simple-http Setup**

* Add `http` app to ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        # ...
        "threadless_router.backends.http",
        # ...
    ]

* Add `simple-http` to ``INSTALLED_BACKENDS``::

    INSTALLED_BACKENDS = {
        # ...
        "simple-http": {
            "ENGINE": "threadless_router.backends.http.outgoing",
            "outgoing_url": 'http://myservice.com/?identity=%(identity)s&text=%(text)s',
        },
        # ...
    }

* Add ``http`` urls::

    urlpatterns = patterns('',
        # ...
        (r'^http/', include('threadless_router.backends.http.urls')),
        # ...
    )

* Now incoming requests will be handled by the http thread::

    >>> import urllib
    >>> import urllib2
    >>> data = urllib.urlencode({'identity': '1112223333', 'text': 'echo hello'})
    >>> urllib2.urlopen('http://localhost:8000/http/simple-http/', data).read()
    'OK'

Celery Support
--------------

``threadless_router`` allows inbound messages to be easily passed off to a
message queue. A celery handler is bundled for example.

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

Development by `Caktus Consulting Group <http://www.caktusgroup.com/>`_.
