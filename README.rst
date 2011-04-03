rapidsms-threadless-router
==========================

A `RapidSMS <https://github.com/rapidsms/rapidsms>`_ router implementation that
removes the threading functionality from the legacy Router class.

httptester
----------

``httptester`` overrides key components in the legacy ``httptester`` app
to provide identical functionality. Django's cache backend is used as dummy storage.

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

Development by `Caktus Consulting Group <http://www.caktusgroup.com/>`_.
