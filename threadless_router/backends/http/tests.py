from django.conf import settings
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse

from threadless_router.backends.http import views
from threadless_router.backends.http.forms import BaseHttpForm


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

    def test_valid_form(self):
        """ Form should be valid if POST keys match configuration """
        view = views.SimpleHttpBackendView(conf=self.conf)
        data = {'phone': '1112223333', 'message': 'hi there'}
        view.request = self.rf.post(self.url, data)
        form = view.get_form(view.get_form_class())
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """ Form is invalid if POST keys don't match configuration """
        view = views.SimpleHttpBackendView(conf=self.conf)
        data = {'invalid-phone': '1112223333', 'invalid-message': 'hi there'}
        view.request = self.rf.post(self.url, data)
        form = view.get_form(view.get_form_class())
        self.assertFalse(form.is_valid())

    def test_invalid_response(self):
        """ HTTP 400 should return if form is invalid """
        data = {'invalid-phone': '1112223333', 'message': 'hi there'}
        response = self._post(data)
        self.assertEqual(response.status_code, 400)

    def test_get_incoming_data(self):
        """ Subclasses must implement get_incoming_data """
        form = BaseHttpForm()
        self.assertRaises(NotImplementedError, form.get_incoming_data)
