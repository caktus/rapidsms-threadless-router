rapidsms-threadless-router
==========================

A `RapidSMS <https://github.com/rapidsms/rapidsms>`_ router implementation that
removes the threading functionality from the legacy Router class.

httptester_cache
----------------

``httptester_cache`` overrides key components in the legacy ``httptester`` app
to provide identical functionality. Django's cache backend used as dummy storage.

* Add `httptester-cache` to ``INSTALLED_BACKENDS``::

    INSTALLED_BACKENDS = {
    # ...
        "httptester-cache": {
            "ENGINE": "threadless_router.backends.httptester_cache.backend",
        },
    # ...
    }

* Update ``RAPIDSMS_TABS`` to reference new view::

    RAPIDSMS_TABS = [
        # ...
        ("threadless_router.backends.httptester_cache.views.generate_identity", "Message Tester"),
        # ...
    ]

* Add or replace existing ``httptester`` urls with ``httptester_cache`` urls::

    urlpatterns = patterns('',
        # ...
        (r'^httptester/', include('threadless_router.backends.httptester_cache.urls')),
        # ...
    )

Development by `Caktus Consulting Group <http://www.caktusgroup.com/>`_.
