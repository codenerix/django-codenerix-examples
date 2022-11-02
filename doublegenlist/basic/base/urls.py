from django.urls import re_path

from .views import InfoList, InfoCreate, InfoDetail, InfoEdit, InfoDelete
from .views import InfoList2, InfoCreate2, InfoDetail2, InfoEdit2, InfoDelete2
from .views import InfoList3, InfoCreate3, InfoDetail3, InfoEdit3, InfoDelete3

urlpatterns = [
    # Info Routes
    re_path("^infos$", InfoList.as_view(), name="info_list"),
    re_path("^infos/add$", InfoCreate.as_view(), name="info_add"),
    re_path("^infos/(?P<pk>\w+)$", InfoDetail.as_view(), name="info_detail"),
    re_path("^infos/(?P<pk>\w+)/edit$", InfoEdit.as_view(), name="info_edit"),
    re_path("^infos/(?P<pk>\w+)/delete$", InfoDelete.as_view(), name="info_delete"),
    # Info 2 Routes
    re_path("^info2s$", InfoList2.as_view(), name="info_list2"),
    re_path("^info2s/add$", InfoCreate2.as_view(), name="info_add2"),
    re_path("^info2s/(?P<pk>\w+)$", InfoDetail2.as_view(), name="info_detail2"),
    re_path("^info2s/(?P<pk>\w+)/edit$", InfoEdit2.as_view(), name="info_edit2"),
    re_path("^info2s/(?P<pk>\w+)/delete$", InfoDelete2.as_view(), name="info_delete2"),
    # Info 3 Routes
    re_path("^info3s$", InfoList3.as_view(), name="info_list3"),
    re_path("^info3s/add$", InfoCreate3.as_view(), name="info_add3"),
    re_path("^info3s/(?P<pk>\w+)$", InfoDetail3.as_view(), name="info_detail3"),
    re_path("^info3s/(?P<pk>\w+)/edit$", InfoEdit3.as_view(), name="info_edit3"),
    re_path("^info3s/(?P<pk>\w+)/delete$", InfoDelete3.as_view(), name="info_delete3"),
]
