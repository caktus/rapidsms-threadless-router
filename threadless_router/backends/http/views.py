from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic.edit import FormMixin, ProcessFormView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rapidsms.log.mixin import LoggerMixin

from threadless_router.base import incoming
from threadless_router.backends.http.forms import HttpForm


class BaseHttpBackendView(FormMixin, LoggerMixin, ProcessFormView):

    http_method_names = ['post']
    conf = None

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(BaseHttpBackendView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.backend_name = kwargs.get('backend_name')
        if self.conf is None:
            self.conf = settings.INSTALLED_BACKENDS[self.backend_name]
        return super(BaseHttpBackendView, self).post(request, *args, **kwargs)

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
