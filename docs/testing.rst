Testing
=======

The benefit of a threadless router is that testing is very easy (and fast).  No
more sleeping until threads join, so tests run at a bearable pace.

No Magic
--------

Need to test using the router? Just instantiate it.  INSTALLED_APPS and
INSTALLED_BACKENDS will be used by default, unless you pass in overrides into
the constructor. For example::

    class MyTest(TestCase):
        def testExample(self):
            backends = {'mockbackend': {"ENGINE": MockBackend}}
            router = Router(backends=backends)

TestScript
----------

RapidSMS provides ``rapidsms.tests.scripted.TestScript`` for testing the entire
stack with transcript-like input. ``threadless_router`` has it's own
``TestScript`` class the provides the same functionality.

By default, any apps within INSTALLED_APPS will be used, but you can also
specific apps for each TestCase.  For example, here's how one can test the
functionality of the ``rapidsms.contrib.default`` app::

    from django.conf import settings

    from rapidsms.apps.base import AppBase
    from rapidsms.contrib.default.app import App as DefaultApp

    from threadless_router.tests.scripted import TestScript


    class OtherApp(AppBase):
        """ Simple application that only responds to a single message """

        name = 'other-app'

        def handle(self, msg):
            if msg.text == 'other-app-should-catch':
                msg.respond('caught')
                return True


    class DefaultTest(TestScript):
        """ Test that rapidsms.contrib.default works properly """

        apps = [OtherApp, DefaultApp]

        def setUp(self):
            super(DefaultTest, self).setUp()
            self._old_message = getattr(settings, 'DEFAULT_RESPONSE', None)

        def tearDown(self):
            super(DefaultTest, self).tearDown()
            if self._old_message:
                settings.DEFAULT_RESPONSE = self._old_message

        def test_full_stack(self):
            """ Test default response functionality alongside other apps """
            message = 'Invalid message, please try again!'
            settings.DEFAULT_RESPONSE = message
            self.runScript("""1112223333 > other-app-should-catch
                              1112223333 < caught
                              1112223333 > uncaught-message-test
                              1112223333 > {0}""".format(message))
