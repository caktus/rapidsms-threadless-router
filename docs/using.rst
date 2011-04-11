Using rapidsms-threadless-router
================================

Caveats and Incompatibilities
-----------------------------

``threadless_router`` can integrate into existing RapidSMS projects.  However,
legacy backends will not work, so you should use the backends bundled with
``threadless_router``, available in the community, or create your own.  As all
routing is handled from within the HTTP thread, non-HTTP backends, such as
``pygsm``, are not (and will never be) compatible with ``threadless_router``.
You should use an HTTP backend with Kannel to achieve the same functionality.

The following legacy RapidSMS applications cannot be used with
``threadless_router``:

* ``rapidsms.contrib.httptester`` - A new :ref:`httptester` is bundled as a
  replacement.
* ``rapidsms.contrib.scheduler`` - The legacy scheduler uses threads to achieve
  crontab-like functionality. Instead, you can use other schedulers such as
  celerybeat.
* ``rapidsms.contrib.ajax``
* ``rapidsms.contrib.messagelog``

.. _httptester:

httptester
----------

``httptester``, bundled with ``threadless_router``, overrides key components in
the legacy ``httptester`` app to provide identical functionality.  Django's
cache backend is used as dummy storage.

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

* Add `httptester` urls::

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
