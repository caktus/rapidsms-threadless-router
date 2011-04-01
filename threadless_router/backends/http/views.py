from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View, FormMixin

from rapidsms.log.mixin import LoggerMixin

from threadless_router.base import incoming


class HttpBackendView(FormMixin, LoggerMixin, View):

    def post(self, request, *args, **kwargs):
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
        return HttpResponseBadRequest()
