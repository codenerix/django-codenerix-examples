from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from agenda.base import urls as base_urls
from agenda.base.views import home, alarms
from agenda.settings import autourl


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^codenerix/', include('codenerix.urls')),

    url('^$', home, name='home'),
    url('^alarmspopups$', alarms, name='alarms'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^base/', include(base_urls)),
]

urlpatterns = autourl(urlpatterns)
