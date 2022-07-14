# -*- coding: utf-8 -*-
from django.urls import re_path as url
from erp.transports.views import TransportZoneList, TransportZoneCreate, TransportZoneCreateModal, TransportZoneUpdate, TransportZoneUpdateModal, TransportZoneDelete, TransportZoneSubList, TransportZoneDetails, TransportZoneDetailModal
from erp.transports.views import TransportRateList, TransportRateCreate, TransportRateCreateModal, TransportRateUpdate, TransportRateUpdateModal, TransportRateDelete, TransportRateSubList, TransportRateDetails, TransportRateDetailModal
from erp.transports.views import TransportCalculate


urlpatterns = [
    url(r'^transportzones$', TransportZoneList.as_view(), name='transportzones_list'),
    url(r'^transportzones/add$', TransportZoneCreate.as_view(), name='transportzones_add'),
    url(r'^transportzones/addmodal$', TransportZoneCreateModal.as_view(), name='transportzones_addmodal'),
    url(r'^transportzones/(?P<pk>\w+)$', TransportZoneDetails.as_view(), name='transportzones_details'),
    url(r'^transportzones/(?P<pk>\w+)/edit$', TransportZoneUpdate.as_view(), name='transportzones_edit'),
    url(r'^transportzones/(?P<pk>\w+)/editmodal$', TransportZoneUpdateModal.as_view(), name='transportzones_editmodal'),
    url(r'^transportzones/(?P<pk>\w+)/delete$', TransportZoneDelete.as_view(), name='transportzones_delete'),
    url(r'^transportzones/(?P<pk>\w+)/sublist$', TransportZoneSubList.as_view(), name='transportzones_sublist'),
    url(r'^transportzones/(?P<pk>\w+)/sublist/add$', TransportZoneCreateModal.as_view(), name='transportzones_sublist_add'),
    url(r'^transportzones/(?P<pk>\w+)/sublist/addmodal$', TransportZoneCreateModal.as_view(), name='transportzones_sublist_addmodal'),
    url(r'^transportzones/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', TransportZoneDetailModal.as_view(), name='transportzones_sublist_details'),
    url(r'^transportzones/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', TransportZoneUpdateModal.as_view(), name='transportzones_sublist_edit'),
    url(r'^transportzones/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', TransportZoneUpdateModal.as_view(), name='transportzones_sublist_editmodal'),
    url(r'^transportzones/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', TransportZoneDelete.as_view(), name='transportzones_sublist_delete'),


    url(r'^transportrates$', TransportRateList.as_view(), name='transportrates_list'),
    url(r'^transportrates/add$', TransportRateCreate.as_view(), name='transportrates_add'),
    url(r'^transportrates/addmodal$', TransportRateCreateModal.as_view(), name='transportrates_addmodal'),
    url(r'^transportrates/(?P<pk>\w+)$', TransportRateDetails.as_view(), name='transportrates_details'),
    url(r'^transportrates/(?P<pk>\w+)/edit$', TransportRateUpdate.as_view(), name='transportrates_edit'),
    url(r'^transportrates/(?P<pk>\w+)/editmodal$', TransportRateUpdateModal.as_view(), name='transportrates_editmodal'),
    url(r'^transportrates/(?P<pk>\w+)/delete$', TransportRateDelete.as_view(), name='transportrates_delete'),
    url(r'^transportrates/(?P<pk>\w+)/sublist$', TransportRateSubList.as_view(), name='transportrates_sublist'),
    url(r'^transportrates/(?P<pk>\w+)/sublist/add$', TransportRateCreateModal.as_view(), name='transportrates_sublist_add'),
    url(r'^transportrates/(?P<pk>\w+)/sublist/addmodal$', TransportRateCreateModal.as_view(), name='transportrates_sublist_addmodal'),
    url(r'^transportrates/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', TransportRateDetailModal.as_view(), name='transportrates_sublist_details'),
    url(r'^transportrates/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', TransportRateUpdateModal.as_view(), name='transportrates_sublist_edit'),
    url(r'^transportrates/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', TransportRateUpdateModal.as_view(), name='transportrates_sublist_editmodal'),
    url(r'^transportrates/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', TransportRateDelete.as_view(), name='transportrates_sublist_delete'),

    url(r'^transport_calculate$', TransportCalculate.as_view(), name='transport_calculate'),
]
