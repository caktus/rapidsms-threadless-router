Changelog
============================================

Below is the history of the rapidsms-threadless-router project. With each release
we note new features, large bug fixes and any backwards incompatible changes.

v0.1.3 (Released 2012-07-25)
------------------------------------

Bug Fixes
_________________________

- Fixed exception when an originary app such as djcelery contains an app module. Thanks to Tim Akinbo.


v0.1.2 (Released 2012-06-29)
------------------------------------

Bug Fixes
_________________________

- Fixed packaging of ``httptester`` templates and css


v0.1.1 (Released 2012-06-28)
------------------------------------

Bug Fixes
_________________________

- Fixed broken packaging due to missing README in the distribution


v0.1.0 (Released 2012-06-28)
------------------------------------

The initial PyPi release.

Features
_________________________

- Replacement HTTP based router
- Working replacements for the ``http``, ``httptester`` and ``kannel`` backends
- Test utilities for writing scripted router tests
- Compatibility layer for processing messages with Celery
