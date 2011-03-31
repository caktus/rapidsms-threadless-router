from django.conf.urls.defaults import *

from threadless_router.backends.httptester_cache import views


urlpatterns = patterns('',
    url(r"^$", views.generate_identity),
    url(r"^(?P<backend_name>[\w-]+)/(?P<identity>\d+)/$", views.message_tester)
)
