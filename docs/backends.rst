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
