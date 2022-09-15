from django.urls import re_path

from .views import InfoList, InfoCreate, InfoDetail, InfoEdit, InfoDelete

urlpatterns = [
    # Info Routes
    re_path("^infos$", InfoList.as_view(), name="info_list"),
    re_path("^infos/add$", InfoCreate.as_view(), name="info_add"),
    re_path("^infos/(?P<pk>\w+)$", InfoDetail.as_view(), name="info_detail"),
    re_path("^infos/(?P<pk>\w+)/edit$", InfoEdit.as_view(), name="info_edit"),
    re_path("^infos/(?P<pk>\w+)/delete$", InfoDelete.as_view(), name="info_delete"),
]
