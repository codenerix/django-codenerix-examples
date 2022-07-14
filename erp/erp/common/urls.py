from django.urls import re_path as url
from .views import PublicContactList, PublicContactCreate, PublicContactCreateModal, PublicContactUpdate, PublicContactUpdateModal, PublicContactDelete, PublicContactDetails


urlpatterns = [
    url(r'^publiccontacts$', PublicContactList.as_view(), name='publiccontacts_list'),
    url(r'^publiccontacts/add$', PublicContactCreate.as_view(), name='publiccontacts_add'),
    url(r'^publiccontacts/addmodal$', PublicContactCreateModal.as_view(), name='publiccontacts_addmodal'),
    url(r'^publiccontacts/(?P<pk>\w+)$', PublicContactDetails.as_view(), name='publiccontacts_details'),
    url(r'^publiccontacts/(?P<pk>\w+)/edit$', PublicContactUpdate.as_view(), name='publiccontacts_edit'),
    url(r'^publiccontacts/(?P<pk>\w+)/editmodal$', PublicContactUpdateModal.as_view(), name='publiccontacts_editmodal'),
    url(r'^publiccontacts/(?P<pk>\w+)/delete$', PublicContactDelete.as_view(), name='publiccontacts_delete'),
]
