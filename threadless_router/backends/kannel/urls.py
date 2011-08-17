from django.conf.urls.defaults import *

from threadless_router.backends.kannel import views


urlpatterns = patterns('',
    url(r"^(?P<backend_name>[\w-]+)/$", views.KannelBackendView.as_view(),
        name='kannel-backend'),
)
