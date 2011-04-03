from django.conf import settings
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse

from threadless_router.backends.http import views


class HttpTest(TestCase):

    urls = 'threadless_router.backends.http.urls'

    def setUp(self):
        self.rf = RequestFactory()
        self.url = reverse('simple-http', args=['simple-http'])
        self.conf = {'incoming_identity': 'phone',
                     'incoming_text': 'message'}
        self.view = views.SimpleHttpBackendView.as_view(conf=self.conf)

    def _post(self, data={}):
        request = self.rf.post(self.url, data)
        return self.view(request, backend_name='simple-http')

    def testValidForm(self):
        view = views.SimpleHttpBackendView(conf=self.conf)
        data = {'phone': '1112223333', 'message': 'hi there'}
        view.request = self.rf.post(self.url, data)
        form = view.get_form(view.get_form_class())
        self.assertTrue(form.is_valid())

    def testInvalidForm(self):
        view = views.SimpleHttpBackendView(conf=self.conf)
        data = {'invalid-phone': '1112223333', 'invalid-message': 'hi there'}
        view.request = self.rf.post(self.url, data)
        form = view.get_form(view.get_form_class())
        self.assertFalse(form.is_valid())

    def testInvalidResponse(self):
        data = {'invalid-phone': '1112223333', 'message': 'hi there'}
        response = self._post(data)
        self.assertEqual(response.status_code, 400)
