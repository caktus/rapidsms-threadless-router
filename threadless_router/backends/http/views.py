from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
from django.views.generic.edit import FormMixin

from rapidsms.log.mixin import LoggerMixin

from threadless_router.base import incoming
from threadless_router.backends.http.forms import HttpForm


class BaseHttpBackendView(FormMixin, LoggerMixin, View):

    conf = {}

    def post(self, request, *args, **kwargs):
        self.backend_name = kwargs.get('backend_name')
        if not self.conf:
            self.conf = settings.INSTALLED_BACKENDS[self.backend_name]
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.debug('form is valid')
        incoming(self.backend_name, **form.get_incoming_data())
        return HttpResponse('OK')

    def form_invalid(self, form):
        self.debug('form failed to validate')
        errors = dict((k, v[0]) for k, v in form.errors.items())
        self.debug(unicode(errors))
        return HttpResponseBadRequest('form failed to validate')


class SimpleHttpBackendView(BaseHttpBackendView):

    form_class = HttpForm

    def get_form_kwargs(self):
        kwargs = super(SimpleHttpBackendView, self).get_form_kwargs()
        kwargs.update({
            'identity': self.conf.get('incoming_identity', 'identity'),
            'text': self.conf.get('incoming_text', 'text'),
        })
        return kwargs
