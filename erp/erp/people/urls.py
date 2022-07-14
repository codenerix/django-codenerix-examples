# -*- coding: utf-8 -*-
from django.urls import re_path as url

from .views import PersonCreateModal, PersonUpdate, PersonUpdateModal, PersonDelete
from .views import (
    CustomerPersonAddressSubList,
    CustomerPersonAddressCreateModal,
    CustomerPersonAddressUpdateModal,
    CustomerPersonAddressSubDelete,
    CustomerPersonAddressDetailsModal,
)
from .views import CustomerPersonAddressSubListBackend
from .views import (
    ProviderPersonAddressSubList,
    ProviderPersonAddressCreateModal,
    ProviderPersonAddressUpdateModal,
    ProviderPersonAddressSubDelete,
    ProviderPersonAddressDetailsModal,
)
from .views import PersonForeign, PersonAuthorStaticPageForeign
from .views import (
    CompanyList,
    CompanyCreate,
    CompanyCreateModal,
    CompanyUpdate,
    CompanyUpdateModal,
    CompanyDelete,
    CompanyForeign,
)
from .views import Profile, ProfileDetails, ProfileUpdate

# from .views import PersonDependentList, PersonDependentCreate, PersonDependentCreateModal, PersonDependentUpdate, PersonDependentUpdateModal, PersonDependentDelete
# from .views import PersonDependentSubList, PersonDependentDetails, PersonDependentDetailsModal
from .views import (
    PersonDocumentSubList,
    PersonDocumentCreateModal,
    PersonDocumentDetailsModal,
    PersonDocumentUpdateModal,
    PersonDocumentDelete,
)
from .views import ServicePersonCreateModal, ServicePersonUpdate
from .views import (
    PublicistList,
    PublicistCreate,
    PublicistCreateModal,
    PublicistUpdateModal,
    PublicistUpdate,
    PublicistSubList,
    PublicistDetails,
    PublicistDetailModal,
    PublicistDelete,
)
from .views import (
    AuthorshipList,
    AuthorshipCreate,
    AuthorshipCreateModal,
    AuthorshipUpdate,
    AuthorshipUpdateModal,
    AuthorshipDelete,
)
from .views import PersonAddressForeignDelivery, PersonAddressForeignInvoice

urlpatterns = [
    url(r"^persons/addmodal$", PersonCreateModal.as_view(), name="people_addmodal"),
    url(r"^persons/(?P<pk>\w+)/edit$", PersonUpdate.as_view(), name="people_edit"),
    url(
        r"^persons/(?P<pk>\w+)/editmodal$",
        PersonUpdateModal.as_view(),
        name="people_editmodal",
    ),
    url(r"^persons/(?P<pk>\w+)/delete$", PersonDelete.as_view(), name="people_delete"),
    url(
        r"^persons/foreign/(?P<search>[\w\W]+|\*)$",
        PersonForeign.as_view(),
        name="people_foreign",
    ),
    url(
        r"^persons/author/foreign/(?P<search>[\w\W]+|\*)$",
        PersonAuthorStaticPageForeign.as_view(),
        name="author_foreign",
    ),
    url(
        r"^servicepersons/addmodal$",
        ServicePersonCreateModal.as_view(),
        name="people_addmodal",
    ),
    url(
        r"^servicepersons/(?P<pk>\w+)/editmodal$",
        ServicePersonUpdate.as_view(),
        name="people_editmodal",
    ),
    url(r"^companys$", CompanyList.as_view(), name="company_list"),
    url(r"^companys/add$", CompanyCreate.as_view(), name="company_add"),
    url(r"^companys/addmodal$", CompanyCreateModal.as_view(), name="company_addmodal"),
    url(r"^companys/(?P<pk>\w+)/edit$", CompanyUpdate.as_view(), name="company_edit"),
    url(
        r"^companys/(?P<pk>\w+)/editmodal$",
        CompanyUpdateModal.as_view(),
        name="company_editmodal",
    ),
    url(
        r"^companys/(?P<pk>\w+)/delete$", CompanyDelete.as_view(), name="company_delete"
    ),
    url(
        r"^companys/foreign/(?P<search>[\w\W]+|\*)$",
        CompanyForeign.as_view(),
        name="company_foreign",
    ),
    url(
        r"^personaddress/(?P<pk>\w+)/customer/sublist$",
        CustomerPersonAddressSubListBackend.as_view(),
        name="customer_personaddress_sublist",
    ),
    url(
        r"^personaddress/(?P<pk>\w+)/customer/sublist/addmodal$",
        CustomerPersonAddressCreateModal.as_view(),
        name="customer_personaddress_add",
    ),
    url(
        r"^personaddress/(?P<tpk>\w+)/customer/sublist/(?P<pk>\w+)$",
        CustomerPersonAddressDetailsModal.as_view(),
        name="customer_personaddress_details",
    ),
    url(
        r"^personaddress/(?P<tpk>\w+)/customer/sublist/(?P<pk>\w+)/editmodal$",
        CustomerPersonAddressUpdateModal.as_view(),
        name="customer_personaddress_edit",
    ),
    url(
        r"^personaddress/(?P<tpk>\w+)/customer/sublist/(?P<pk>\w+)/delete$",
        CustomerPersonAddressSubDelete.as_view(),
        name="customer_personaddress_delete",
    ),
    url(
        r"^personaddress/(?P<pk>\w+)/cliente/sublist$",
        CustomerPersonAddressSubList.as_view(),
        name="customer_personaddress_sublist_frontend",
    ),
    url(
        r"^personaddress/(?P<pk>\w+)/cliente/sublist/addmodal$",
        CustomerPersonAddressCreateModal.as_view(),
        name="customer_personaddress_add_frontend",
    ),
    url(
        r"^personaddress/(?P<tpk>\w+)/cliente/sublist/(?P<pk>\w+)$",
        CustomerPersonAddressDetailsModal.as_view(),
        name="customer_personaddress_details_frontend",
    ),
    url(
        r"^personaddress/(?P<tpk>\w+)/cliente/sublist/(?P<pk>\w+)/editmodal$",
        CustomerPersonAddressUpdateModal.as_view(),
        name="customer_personaddress_edit_frontend",
    ),
    url(
        r"^personaddress/(?P<tpk>\w+)/cliente/sublist/(?P<pk>\w+)/delete$",
        CustomerPersonAddressSubDelete.as_view(),
        name="customer_personaddress_delete_frontend",
    ),
    url(
        r"^personaddress/foreign/d/(?P<search>[\w\W]+|\*)$",
        PersonAddressForeignDelivery.as_view(),
        name="personaddress_foreign_delivery",
    ),
    url(
        r"^personaddress/foreign/i/(?P<search>[\w\W]+|\*)$",
        PersonAddressForeignInvoice.as_view(),
        name="personaddress_foreign_invoice",
    ),
    url(
        r"^personaddress/(?P<pk>\w+)/provider/sublist$",
        ProviderPersonAddressSubList.as_view(),
        name="provider_personaddress_sublist",
    ),
    url(
        r"^personaddress/(?P<pk>\w+)/provider/sublist/addmodal$",
        ProviderPersonAddressCreateModal.as_view(),
        name="provider_personaddress_add",
    ),
    url(
        r"^personaddress/(?P<tpk>\w+)/provider/sublist/(?P<pk>\w+)$",
        ProviderPersonAddressDetailsModal.as_view(),
        name="provider_personaddress_details",
    ),
    url(
        r"^personaddress/(?P<tpk>\w+)/provider/sublist/(?P<pk>\w+)/editmodal$",
        ProviderPersonAddressUpdateModal.as_view(),
        name="provider_personaddress_edit",
    ),
    url(
        r"^personaddress/(?P<tpk>\w+)/provider/sublist/(?P<pk>\w+)/delete$",
        ProviderPersonAddressSubDelete.as_view(),
        name="provider_personaddress_delete",
    ),
    url(r"^profiles$", Profile.as_view(), name="profile_list"),
    url(r"^profiles/(?P<pk>\w+)$", ProfileDetails.as_view(), name="profile_details"),
    url(r"^profiles/(?P<pk>\w+)/edit$", ProfileUpdate.as_view(), name="profile_edit"),
    url(
        r"^persondocuments/(?P<pk>\w+)/sublist$",
        PersonDocumentSubList.as_view(),
        name="persondocuments_sublist",
    ),
    url(
        r"^persondocuments/(?P<pk>\w+)/sublist/addmodal$",
        PersonDocumentCreateModal.as_view(),
        name="persondocuments_sublist_addmodal",
    ),
    url(
        r"^persondocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$",
        PersonDocumentDetailsModal.as_view(),
        name="persondocuments_sublist_details",
    ),
    url(
        r"^persondocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$",
        PersonDocumentUpdateModal.as_view(),
        name="persondocuments_sublist_editmodal",
    ),
    url(
        r"^persondocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$",
        PersonDocumentDelete.as_view(),
        name="persondocuments_sublist_delete",
    ),
    url(r"^publicists$", PublicistList.as_view(), name="publicists_list"),
    url(r"^publicists/add$", PublicistCreate.as_view(), name="publicists_add"),
    url(
        r"^publicists/addmodal$",
        PublicistCreateModal.as_view(),
        name="publicists_addmodal",
    ),
    url(
        r"^publicists/(?P<pk>\w+)$",
        PublicistDetails.as_view(),
        name="publicists_details",
    ),
    url(
        r"^publicists/(?P<pk>\w+)/edit$",
        PublicistUpdate.as_view(),
        name="publicists_edit",
    ),
    url(
        r"^publicists/(?P<pk>\w+)/editmodal$",
        PublicistUpdateModal.as_view(),
        name="publicists_editmodal",
    ),
    url(
        r"^publicists/(?P<pk>\w+)/delete$",
        PublicistDelete.as_view(),
        name="publicists_delete",
    ),
    url(
        r"^publicists/(?P<pk>\w+)/sublist$",
        PublicistSubList.as_view(),
        name="publicists_sublist",
    ),
    url(
        r"^publicists/(?P<pk>\w+)/sublist/add$",
        PublicistCreateModal.as_view(),
        name="publicists_sublist_add",
    ),
    url(
        r"^publicists/(?P<pk>\w+)/sublist/add$modal",
        PublicistCreateModal.as_view(),
        name="publicists_sublist_addmodal",
    ),
    url(
        r"^publicists/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$",
        PublicistDetailModal.as_view(),
        name="publicists_sublist_details",
    ),
    url(
        r"^publicists/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$",
        PublicistUpdateModal.as_view(),
        name="publicists_sublist_edit",
    ),
    url(
        r"^publicists/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$",
        PublicistUpdateModal.as_view(),
        name="publicists_sublist_editmodal",
    ),
    url(
        r"^publicists/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$",
        PublicistDelete.as_view(),
        name="publicists_sublist_delete",
    ),
    url(r"^authorships$", AuthorshipList.as_view(), name="authorships_list"),
    url(r"^authorships/add$", AuthorshipCreate.as_view(), name="authorships_add"),
    url(
        r"^authorships/addmodal$",
        AuthorshipCreateModal.as_view(),
        name="authorships_addmodal",
    ),
    url(
        r"^authorships/(?P<pk>\w+)/edit$",
        AuthorshipUpdate.as_view(),
        name="authorships_edit",
    ),
    url(
        r"^authorships/(?P<pk>\w+)/editmodal$",
        AuthorshipUpdateModal.as_view(),
        name="authorships_editmodal",
    ),
    url(
        r"^authorships/(?P<pk>\w+)/delete$",
        AuthorshipDelete.as_view(),
        name="authorships_delete",
    ),
]
