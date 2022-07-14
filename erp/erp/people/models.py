# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models, transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str

from codenerix.models import Log, CodenerixModel
from codenerix.models_people import GenPerson, GenRole

from codenerix_geodata.models import GeoAddress
from codenerix_extensions.validators import spanishNIFNIECIF
from codenerix_invoicing.models_sales import GenCustomer, GenAddressDelivery, GenAddressInvoice
from codenerix_invoicing.models_purchases import GenProvider
from codenerix_storages.models import GenStorageOperator
from codenerix_pos.models import GenPOSOperator
from codenerix_cms.models import GenStaticPageAuthor
from codenerix_corporate.models import CorporateImage

from erp.base.models import LANG_CHOICE
from erp.people.settings import CDNX_PERMISSIONS

DOCUMENT_TYPES_DNI = 'D'
DOCUMENT_TYPES_NIE = 'N'
DOCUMENT_TYPES_CIF = 'C'
DOCUMENT_TYPES = (
    ('U', _('Unspecified')),
    ('P', _('Passport')),
    (DOCUMENT_TYPES_DNI, _('DNI')),
    (DOCUMENT_TYPES_NIE, _('NIE')),
    (DOCUMENT_TYPES_CIF, _('CIF')),
)


# ############################
class Person(CodenerixModel, GenProvider, GenCustomer, GenPOSOperator, GenStorageOperator, GenPerson):
    # Personal information
    nid = models.CharField(_("NID"), max_length=20, blank=True, validators=[spanishNIFNIECIF])
    nid_type = models.CharField(_("NID Type"), max_length=1, choices=DOCUMENT_TYPES, default='U')
    birthdate = models.DateField(_("Birthdate"), blank=True, null=True)
    lang = models.CharField(_("Language"), max_length=2, choices=LANG_CHOICE, blank=False, null=False)
    phone = models.CharField(_("Phone"), max_length=16, blank=True, null=True)

    def __fields__(self, info):
        fields = super(Person, self).__fields__(info)
        fields.append(('nid', _('NID')))
        fields.append(('phone', _('Phone')))
        return fields

    def __searchQ__(self, info, text):
        tf = super(Person, self).__searchQ__(info, text)
        tf['nid'] = Q(nid__icontains=text)
        tf['address'] = Q(address__icontains=text)
        tf['phone'] = Q(phone__icontains=text)
        return tf

    @staticmethod
    def validate_nid(nid, nid_type):
        if nid and nid_type and nid_type in [DOCUMENT_TYPES_NIE, DOCUMENT_TYPES_DNI, DOCUMENT_TYPES_CIF]:
            kind = {
                'nif': False,
                'nie': False,
                'cif': False
            }
            if nid_type == DOCUMENT_TYPES_NIE:
                kind['nie'] = True
            elif nid_type == DOCUMENT_TYPES_DNI:
                kind['nif'] = True
            else:
                kind['cif'] = True
            func = spanishNIFNIECIF(**kind)
            try:
                func(nid)
            except ValidationError as e:
                return e
        return None

    def save(self, *args, **kwards):
        error = Person.validate_nid(self.nid, self.nid_type)
        if error:
            raise ValidationError(error)
        else:
            error = self.__nid_unique()
            if error:
                raise ValidationError(error)

        return super(Person, self).save(*args, **kwards)

    def __nid_unique(self):
        error = None
        if self.nid and Person.objects.filter(nid=self.nid).exclude(pk=self.pk).exists():
            error = _('NID duplicated')
        return error

    def is_posoperator(self):
        return hasattr(self, 'pos_operator')

    def is_storageoperator(self):
        return hasattr(self, 'storage_operator')

    def is_publicist(self):
        return hasattr(self, 'publicists')

    @property
    def billing_address(self):
        try:
            address = PersonAddress.object.get(person=self, main=True)
            return address
        except ObjectDoesNotExist:
            return None

    def get_people(self):
        if self.is_admin():
            return Person.objects.all().distinct()
        else:
            return Person.objects.select_related().distinct()

    def is_manager(self):
        return hasattr(self, 'managers')

    def is_buyer(self):
        return hasattr(self, 'buyers')

    def AutoCleanUser(self):
        if self.user and self.user.pk:
            # delete person if not roles
            user = self.user
            with transaction.atomic():
                self.delete()
                # delete user if not log
                if Log.objects.filter(user_id=user).count() == 0:
                    user.delete()

    # bridge to Customers
    def CDNX_get_fk_info_customer(self):
        return {'label': _("Person"), 'related': "people_foreign"}

    def __fields_customer__(self, info, fields):
        fields = []
        fields.append(('external__nid', _('Nid')))
        fields.append(('external__user__username', _('Username')))
        fields.append(('external__surname', _('Surname')))
        fields.append(('external__name', _('Name')))
        fields.append(('external__user__email', _('Email')))
        fields.append(('external__phone', _('Phone')))
        return fields

    def CDNX_get_details_info_customer(self):
        fields = [
            (
                _('Info customer'), 6,
                ['customer__external__user__username', 6],
                ['customer__external__surname', 6],
                ['customer__external__name', 6],
                ['customer__external__user__email', 6],
                ['customer__external__nid', 6],
                ['customer__external__phone', 6],
            ), (
                _('Address delivery'), 6,
                ['budget__address_delivery', 6],
            ), (
                _('Address invoice'), 6,
                ['budget__address_invoice', 6],
            )
        ]
        return fields

    # bridge to Provider
    def CDNX_get_fk_info_provider(self):
        return {'label': _("Person"), 'related': "people_foreign"}

    def __fields_provider__(self, info, fields):
        fields.insert(0, ('external__nid', _('Nid')))
        fields.insert(0, ('external__user__username', _('Username')))
        fields.insert(0, ('external__surname', _('Surname')))
        fields.insert(0, ('external__name', _('Name')))
        fields.insert(0, ('external__user__email', _('Email')))
        return fields

    def CDNX_get_email(self):
        if hasattr(self.user, 'email'):
            return self.user.email
        else:
            return None

    # bridge to POSOperator
    def CDNX_get_fk_info_posoperator(self):
        return {'label': _("Person"), 'related': "people_foreign"}

    def __fields_posoperator__(self, info, fields):
        fields.insert(0, ('external__nid', _('Nid')))
        fields.insert(0, ('external__user__username', _('Username')))
        fields.insert(0, ('external__surname', _('Surname')))
        fields.insert(0, ('external__name', _('Name')))
        fields.insert(0, ('external__user__email', _('Email')))
        return fields

    # bridge to POSOperator
    def CDNX_get_fk_info_storage_operator(self):
        return {'label': _("Person"), 'related': "people_foreign"}

    def __fields_storage__(self, info, fields):
        fields.insert(0, ('external__nid', _('Nid')))
        fields.insert(0, ('external__user__username', _('Username')))
        fields.insert(0, ('external__surname', _('Surname')))
        fields.insert(0, ('external__name', _('Name')))
        fields.insert(0, ('external__user__email', _('Email')))
        return fields


# Person Address
class PersonAddress(CodenerixModel, GeoAddress, GenAddressDelivery, GenAddressInvoice):
    person = models.ForeignKey(Person, related_name='addresses', verbose_name=_("Person"), on_delete=models.CASCADE)
    alias = models.CharField(_("Alias"), max_length=100, blank=True, null=True)
    mobile_phone = models.CharField(_("Mobile Phone"), max_length=16, blank=True, null=True)
    main_delivery = models.BooleanField(_("Main delivery"), max_length=250, null=False, default=False)
    main_invoice = models.BooleanField(_("Main invoice"), max_length=250, null=False, default=False)

    def __unicode__(self):
        name = ''
        if self.alias:
            name = u'{} ({}, {})'.format(self.alias, self.address, self.zipcode)
        else:
            name = u'{}, {}'.format(self.address, self.zipcode)
        return name

    def get_summary(self):
        address = u""
        if self.city:
            address += u"{}\n".format(self.city)
        address += u"{}, {}".format(self.address, self.zipcode)
        if self.phone and self.mobile_phone:
            address += u" {} / {}".format(self.phone, self.mobile_phone)
        elif self.phone:
            address += u" {}".format(self.phone)
        elif self.mobile_phone:
            address += u" {}".format(self.mobile_phone)
        return address

    # bridge to Address
    def CDNX_get_fk_info_address_delivery(self):
        return {'label': _("Address"), 'related': "personaddress_foreign_delivery"}

    def CDNX_get_fk_info_address_invoice(self):
        return {'label': _("Address"), 'related': "personaddress_foreign_invoice"}

    def __fields__(self, info):
        fields = super(PersonAddress, self).__fields__(info)
        fields.insert(0, ('person', _('Person')))
        fields.insert(0, ('alias', _('Alias')))
        fields.append(('mobile_phone', _("Mobile Phone")))
        fields.append(('main_delivery', _("Main delivery")))
        fields.append(('main_invoice', _("Main invoice")))
        return fields

    def save(self, *args, **kwards):
        with transaction.atomic():
            if self.main_delivery:
                PersonAddress.objects.exclude(pk=self.pk).filter(person=self.person).update(main_delivery=False)
            elif not PersonAddress.objects.exclude(pk=self.pk).filter(person=self.person).filter(main_delivery=True).exists():
                self.main_delivery = True
            elif PersonAddress.objects.exclude(pk=self.pk).filter(person=self.person).count() == 0:
                self.main_delivery = True

            if self.main_invoice:
                PersonAddress.objects.exclude(pk=self.pk).filter(person=self.person).update(main_invoice=False)
            elif not PersonAddress.objects.exclude(pk=self.pk).filter(person=self.person).filter(main_invoice=True).exists():
                self.main_invoice = True
            elif PersonAddress.objects.exclude(pk=self.pk).filter(person=self.person).count() == 0:
                self.main_invoice = True
        return super(PersonAddress, self).save(*args, **kwards)


class Company(CodenerixModel):  # , GenStorage, GenStorageContact):  # , GenPOSCompany):
    corporate_image = models.OneToOneField(CorporateImage, related_name='companies', verbose_name=_("Corporate Image"), on_delete=models.CASCADE)
    active = models.BooleanField(_("Active"), blank=False, default=True)

    def __fields__(self, info):
        return [
            ('corporate_image', _("Person")),
            ('active', _("Active")),
        ]

    def __str__(self):
        return str(self.corporate_image)

    def __unicode__(self):
        return self.__str__()

"""
    # bridge to Storages
    def CDNX_get_fk_info_storage(self):
        return {'label': _("Company"), 'related': "company_foreign"}

    def __fields_storage__(self, info, fields):
        fields.append(('external__person__nid', _('Nid')))
        fields.append(('external__active', _('Active')))
        fields.insert(0, ('external__person__user__username', _('Username')))
        fields.insert(0, ('external__person__surname', _('Surname')))
        fields.insert(0, ('external__person__name', _('Name')))
        fields.insert(0, ('external__person__user__email', _('Email')))
        return fields

    # bridge to Storages contact
    def CDNX_get_fk_info_storage_contacts(self):
        return {'label': _("Company"), 'related': "company_foreign"}

    def __fields_storage_contacts__(self, info, fields):
        fields.insert(0, ('external_contact__person__user__username', _('Username')))
        fields.insert(0, ('external_contact__person__surname', _('Surname')))
        fields.insert(0, ('external_contact__person__name', _('Name')))
        fields.insert(0, ('external_contact__person__user__email', _('Email')))
        return fields

    # bridge to Invoice Pos
    def CDNX_get_fk_info_invoicing_pos(self):
        return {'label': _("Company"), 'related': "company_foreign"}

    def __fields_invoicing_pos__(self, info, fields):
        fields.append(('external', _('Company')))
        return fields
"""


# ############################
class Publicist(GenRole, CodenerixModel):
    class CodenerixMeta:
        rol_groups = {
            'Publicist': CDNX_PERMISSIONS['publicist'],
        }

    person = models.OneToOneField(Person, related_name='publicists', verbose_name=_("Person"), null=False, on_delete=models.CASCADE, blank=False)
    enable = models.BooleanField(_("Enable"), blank=False, null=False, default=True)

    def __unicode__(self):
        return u"{} ({})".format(smart_str(self.person), self.enable)

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('person', _("Person")))
        fields.append(('enable', _("Enable")))
        return fields


# ############################
class Authorship(GenStaticPageAuthor, CodenerixModel):
    person = models.ForeignKey(Person, related_name="authors", blank=False, null=False, on_delete=models.CASCADE)

    # bridge to Static Page
    def CDNXCMS_get_fk_info_author(self):
        return {'label': _("Author"), 'related': "author_foreign"}

    @staticmethod
    def CDNXCMS_get_name_related():
        return 'person'

    def CDNXCMS_get_summary(self):
        return self.person.__unicode__()

    def __fields_staticpage__(self, info):
        fields = []
        fields.append(('person__nid', _('Nid')))
        fields.append(('person__user__username', _('Username')))
        fields.append(('person__surname', _('Surname')))
        fields.append(('person__name', _('Name')))
        fields.append(('person__user__email', _('Email')))
        return fields

    def __fields__(self, info):
        fields = []
        fields.append(('person__nid', _('Nid')))
        fields.append(('person__user__username', _('Username')))
        fields.append(('person__surname', _('Surname')))
        fields.append(('person__name', _('Name')))
        fields.append(('person__user__email', _('Email')))
        return fields
