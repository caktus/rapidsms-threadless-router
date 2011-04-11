.. rapidsms-threadless-router documentation master file, created by
   sphinx-quickstart on Sun Apr 10 17:44:26 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

rapidsms-threadless-router
==========================

A `RapidSMS <https://github.com/rapidsms/rapidsms>`_ router implementation that
removes the threading functionality from the legacy Router class.  Rather, all
inbound requests are handled via the main HTTP thread.  Backends can optionally
pass requests to a message queue for out-of-band responses.
``threadless_router`` attempts to:

* Make RapidSMS backends more Django-like.  Use Django's URL routing and views to handle inbound HTTP requests.
* Remove clutter and complexity of route process and threaded backends.
* Ease testing -- no more ``threading`` or ``Queue`` modules slowing down tests.


Contents:

.. toctree::
   :maxdepth: 2
   
   works
   using
   queue
   testing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

