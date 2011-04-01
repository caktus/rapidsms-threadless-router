from threadless_router.backends.http.views import HttpBackendView


class TwilioBackendView(HttpBackendView):

    form = TwilioForm
