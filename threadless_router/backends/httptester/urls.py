from django.conf.urls.defaults import *

from threadless_router.backends.httptester import views


urlpatterns = patterns('',
    url(r"^(?P<backend_name>[\w-]+)/$", views.generate_identity),
    url(r"^(?P<backend_name>[\w-]+)/(?P<identity>\d+)/$", views.message_tester)
)
