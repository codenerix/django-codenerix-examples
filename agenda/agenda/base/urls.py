from django.urls import re_path

from .views import ContactList, ContactCreate, ContactDetail, ContactEdit, ContactDelete, ContactForeign
from .views import PhoneList, PhoneCreate, PhoneDetail, PhoneEdit, PhoneDelete
from .views import ContactGroupList, ContactGroupCreate, ContactGroupDetail, ContactGroupEdit, ContactGroupDelete


urlpatterns = [
    # Contacts Routes
    re_path('^contacts$', ContactList.as_view(), name='contact_list'),
    re_path('^contacts/add$', ContactCreate.as_view(), name='contact_add'),
    re_path('^contacts/(?P<pk>\w+)$', ContactDetail.as_view(), name='contact_detail'),
    re_path('^contacts/(?P<pk>\w+)/edit$', ContactEdit.as_view(), name='contact_edit'),
    re_path('^contacts/(?P<pk>\w+)/delete$', ContactDelete.as_view(), name='contact_delete'),
    re_path('^contacts/(?P<search>[\w\W]+|\*)$', ContactForeign.as_view(), name='contact_foreign'),

    # Phones Routes
    re_path('^phones/(?P<pk>\w+)/sublist$', PhoneList.as_view(), name='phone_sublist'),
    re_path('^phones/(?P<pk>\w+)/sublist/addmodal$', PhoneCreate.as_view(), name='phone_sublist_add'),
    re_path('^phones/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', PhoneDetail.as_view(), name='phone_sublist_detail'),
    re_path('^phones/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', PhoneEdit.as_view(), name='phone_sublist_edit'),
    re_path('^phones/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', PhoneDelete.as_view(), name='phone_sublist_delete'),

    # ContactGroups Routes
    re_path('^contactgroups$', ContactGroupList.as_view(), name='contactgroup_list'),
    re_path('^contactgroups/add$', ContactGroupCreate.as_view(), name='contactgroup_add'),
    re_path('^contactgroups/(?P<pk>\w+)$', ContactGroupDetail.as_view(), name='contactgroup_detail'),
    re_path('^contactgroups/(?P<pk>\w+)/edit$', ContactGroupEdit.as_view(), name='contactgroup_edit'),
    re_path('^contactgroups/(?P<pk>\w+)/delete$', ContactGroupDelete.as_view(), name='contactgroup_delete'),
]
