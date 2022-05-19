from django.conf.urls import include
from django.urls import re_path
from django.contrib.auth.views import LoginView, LogoutView


from agenda.base import urls as base_urls
from agenda.base.views import home, alarms
from agenda.settings import autourl


urlpatterns = [
    re_path(r'^codenerix/', include('codenerix.urls')),

    re_path('^$', home, name='home'),
    re_path('^alarmspopups$', alarms, name='alarms'),
    re_path(r'^login/$', LoginView.as_view(), name='login'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),

    re_path(r'^base/', include(base_urls)),
]

urlpatterns = autourl(urlpatterns)
