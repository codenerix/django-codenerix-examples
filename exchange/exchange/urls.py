from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from exchange.base import urls as base_urls
from exchange.base.views import alarms, status
from exchange.settings import autourl


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', RedirectView.as_view(url=reverse_lazy('exchange_list'), permanent=True), name='home'),
    url('^alarmspopups$', alarms, name='alarms'),
    url(r'^status/(?P<status>\w+)/(?P<answer>[a-zA-Z0-9+/]+)$', status, name='status'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^base/', include(base_urls)),
]

urlpatterns = autourl(urlpatterns)
