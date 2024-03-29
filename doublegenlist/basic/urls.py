from django.conf.urls import include
from django.urls import re_path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView
from django.urls import reverse_lazy

from basic.base import urls as base_urls
from basic.base2 import urls as base2_urls
from basic.base.views import alarms
from basic.settings import autourl


urlpatterns = [
    re_path(r"^codenerix/", include("codenerix.urls")),
    re_path(
        "^$",
        RedirectView.as_view(url=reverse_lazy("info_list"), permanent=True),
        name="home",
    ),
    re_path("^alarmspopups$", alarms, name="alarms"),
    re_path(r"^login/$", LoginView.as_view(), name="login"),
    re_path(r"^logout/$", LogoutView.as_view(), name="logout"),
    re_path(r"^base/", include(base_urls)),
    re_path(r"^base2/", include(base2_urls)),
]

urlpatterns = autourl(urlpatterns)
