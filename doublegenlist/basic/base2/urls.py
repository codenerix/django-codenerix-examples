from django.urls import re_path

from .views import InfoListB1, InfoCreateB1, InfoDetailB1, InfoEditB1, InfoDeleteB1
from .views import InfoListB2, InfoCreateB2, InfoDetailB2, InfoEditB2, InfoDeleteB2

urlpatterns = [
    # Info 4 Routes
    re_path("^infos$", InfoListB1.as_view(), name="info_listb1"),
    re_path("^infos/add$", InfoCreateB1.as_view(), name="info_addb1"),
    re_path("^infos/(?P<pk>\w+)$", InfoDetailB1.as_view(), name="info_detailb1"),
    re_path("^infos/(?P<pk>\w+)/edit$", InfoEditB1.as_view(), name="info_editb1"),
    re_path("^infos/(?P<pk>\w+)/delete$", InfoDeleteB1.as_view(), name="info_deleteb1"),
    # Info 4 Routes
    re_path("^info2s$", InfoListB2.as_view(), name="info_listb2"),
    re_path("^info2s/add$", InfoCreateB2.as_view(), name="info_addb2"),
    re_path("^info2s/(?P<pk>\w+)$", InfoDetailB2.as_view(), name="info_detailb2"),
    re_path("^info2s/(?P<pk>\w+)/edit$", InfoEditB2.as_view(), name="info_editb2"),
    re_path(
        "^info2s/(?P<pk>\w+)/delete$", InfoDeleteB2.as_view(), name="info_deleteb2"
    ),
]
