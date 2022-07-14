# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.forms import Form
from django.contrib.auth.models import User
from django.forms.forms import NON_FIELD_ERRORS
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import ProgrammingError

from codenerix.forms import GenModelForm
from codenerix_extensions.helpers import get_language_database
from codenerix_geodata.models import Country, Province
from codenerix_invoicing.models import BillingSeries

from .models import Person, PersonAddress, Company, Publicist, Authorship


class LoginForm(AuthenticationForm):
    class Meta:
        password = forms.CharField(widget=forms.PasswordInput)
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


def get_country():
    lang = get_language_database()
    result = []
    try:
        countries = Country.objects.all().order_by(*['{}__name'.format(lang)])
        for country in countries:
            result.append((country.pk, str(country)))
    except ProgrammingError as e:
        print(e)
    return result


def get_provinces():
    lang = get_language_database()
    result = []
    # for province in Province.objects.filter(region__country__code='ES').order_by('es__name'):
    try:
        for province in Province.objects.all().order_by(*['{}__name'.format(lang)]):
            result.append((province.pk, str(province)))
    except ProgrammingError as e:
        print(e)
    return result


class CustomerRegisterForm(Form):
    name = forms.CharField(label=_("Name"), min_length=2, max_length=45, required=True)
    surname = forms.CharField(label=_("Surname"), min_length=2, max_length=90, required=True)
    email = forms.EmailField(label=_("E-Mail"), min_length=2, max_length=128, required=True)
    password1 = forms.CharField(label=_("Password"), min_length=8, widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label=_("Confirm password"), min_length=8, widget=forms.PasswordInput, required=True)
    address = forms.CharField(label=_("Address"), min_length=2, max_length=250, required=True)
    country = forms.ChoiceField(label=_("Country"), choices=get_country(), required=True, widget=forms.Select(attrs={'class': 'form-control c-square c-theme'}))
    # province = forms.ChoiceField(label=_("Province"), choices=get_provinces(), required=True, widget=forms.Select())
    province = forms.CharField(label=_("Province"), max_length=2, required=False, widget=forms.HiddenInput())
    town = forms.CharField(label=_("Town"), min_length=2, max_length=250, required=True)
    zipcode = forms.CharField(label=_("Zip code"), max_length=6, required=True)
    phone = forms.CharField(label=_("Phone"), max_length=16, required=True)

    # check email no repeated
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
            raise forms.ValidationError(_("Email or user alredy exist"))
        except ObjectDoesNotExist:
            return email

    # check correct password confirm
    # check if billing serie exist
    def clean(self):
        cleaned_data = super(CustomerRegisterForm, self).clean()

        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError(_("Passwords do not match"))

        billing = BillingSeries.objects.filter(default=True).first()
        if not billing:
            raise forms.ValidationError(_("There is an error with registration system, please contact with administration. (Missing BS)"))


class PersonFormOnly(GenModelForm):
    email = forms.EmailField(label=_('Email'), required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        exclude = ['user', 'creator', 'customer', 'provider', 'pos_operator', 'disabled', 'lang', 'storage_operator', 'storage_zone_operable']
        model = Person

    def __groups__(self):
        return [
            (
                _('Personal data'), 12,
                ['name', 6],
                ['surname', 6],
                ['email', 6],
                ['phone', 6],
                ['nid', 6],
                ['nid_type', 6],
                ['birthdate', 6],
                ['phone', 6],
            ),
        ]

    @staticmethod
    def __groups_details__():
        return [
            (
                _('Personal data'), 12,
                ['name', 6],
                ['surname', 6],
                ['user__email', 6],
                ['nid', 6],
                ['nid_type', 6],
                ['birthdate', 6],
                ['phone', 6],
            ),
        ]


class PersonForm(GenModelForm):
    username = forms.CharField(label=_('Username'), required=False, min_length=settings.USERNAME_MIN_SIZE, widget=forms.TextInput(attrs={'placeholder': _('Username'), 'class': 'form-control'}))
    password = forms.CharField(label=_('New password'), required=False, min_length=settings.PASSWORD_MIN_SIZE, widget=forms.PasswordInput(attrs={'placeholder': _('New password'), 'class': 'form-control'}))
    confirm = forms.CharField(label=_('Confirm password'), required=False, min_length=settings.PASSWORD_MIN_SIZE, widget=forms.PasswordInput(attrs={'placeholder': _('Confirm password'), 'class': 'form-control'}))
    email = forms.EmailField(label=_('Email'), required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        exclude = ['lang', 'user', 'creator', 'customer', 'provider', 'pos_operator', 'storage_operator', 'storage_zone_operable']
        model = Person

    def __groups__(self):
        return [
            (
                _('Personal data'), 6,
                ['name', 6],
                ['surname', 6],
                ['nid', 6],
                ['nid_type', 6],
                ['birthdate', 6],
                ['phone', 6],
            ),
            (
                _('System access (Optional)'), 6,
                ['username', 6],
                ['email', 6],
                ['password', 6],
                ['confirm', 6],
                ['disabled', 6],
            ),
        ]

    @staticmethod
    def __groups_details__():
        return [
            (
                _('System access'), 6,
                ['username', 6],
                ['email', 6],
                ['password', 6],
                ['confirm', 6],
                ['disabled', 6],
            ),
            (
                _('Personal data'), 6,
                ['name', 6],
                ['surname', 6],
                ['nid', 6],
                ['nid_type', 6],
                ['lang', 6],
                ['birthdate', 6],
            ),
        ]

    def clean(self):
        # Initilization
        error = False

        # Get form,_data
        form_data = self.cleaned_data

        nid = form_data.get('nid', None)
        nid_type = form_data.get('nid_type', None)

        err = Person.validate_nid(nid, nid_type)
        if err:
            self._errors["nid_type"] = err
            error = True

        if error is False:
            # Check if we got the username
            if self.Meta.in_user:

                # Initilization
                error = False

                # Get fields
                email = form_data.get("email", None)
                password = form_data.get("password", None)
                confirm = form_data.get("confirm", None)

                # Check email
                if not email:
                    # Email is required
                    self._errors["email"] = [_("This field is required")]
                    error = True

                # Check password
                if (not password or not confirm) and (password != confirm):
                    self._errors["password"] = [_("Passwords do not match")]
                    self._errors["confirm"] = [_("Passwords do not match")]
                    error = True

            else:

                if form_data.get("username", None):

                    # Check username
                    if User.objects.filter(username=form_data['username']).count() > 0:
                        # Username already in use
                        self._errors["username"] = [_("Username already in use")]
                        error = True

                    # Get fields
                    email = form_data.get("email", None)
                    password = form_data.get("password", None)
                    confirm = form_data.get("confirm", None)

                    # Check email
                    if not email:
                        # Email is required
                        self._errors["email"] = [_("Required for new users")]
                        error = True

                    # Check password
                    if not password:
                        self._errors["password"] = [_("Required for new users")]
                        error = True

                    # Check confirm
                    if not confirm:
                        # Confirm is required
                        self._errors["confirm"] = [_("Required for new users")]
                        error = True

                    # Check password
                    if password and confirm and (password != confirm):
                        self._errors["password"] = [_("Passwords do not match")]
                        self._errors["confirm"] = [_("Passwords do not match")]
                        error = True

                else:
                    # If we didn't get the usernamem clean up all fields connected with it
                    error = []
                    for field, trans in [
                        ('password', [_('Password')]),
                        ('confirm', [_('Confirmation')]),
                        ('email', [_('Email')])
                    ]:
                        if form_data.get(field, None):
                            error.append(trans)

                    # If some error detected, notify the user
                    if error:
                        msg = self.errors.get(NON_FIELD_ERRORS, [])
                        msg.append(_("You have specified '%(field)s', if you want to assign a new user you must fill the username field, otherwise leave 'Password, Confirmation and Email' empty" % {'field': " - ".join(error[0])}))
                        self._errors[NON_FIELD_ERRORS] = msg

        # If some error happened, delete content from this fields
        if error:
            if 'password' in form_data:
                del form_data['password']
            if 'confirm' in form_data:
                del form_data['confirm']

        # Return form_data
        return form_data


class PersonFormForService(GenModelForm):
    email = forms.EmailField(label=_('Email'), required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        exclude = ['lang', 'disabled', 'user', 'creator', 'customer', 'provider', 'pos_operator', 'storage_operator', 'storage_zone_operable']
        model = Person

    def __groups__(self):
        return [
            (
                _('Personal data'), 12,
                ['name', 6],
                ['surname', 6],
                ['nid', 6],
                ['nid_type', 6],
                ['birthdate', 6],
                ['email', 6],
                ['phone', 6],
            ),
        ]


class PersonAddressForm(GenModelForm):
    country = forms.CharField(label=_('Country'), required=True)
    region = forms.CharField(label=_('Region'), required=True)
    province = forms.CharField(label=_('Province'), required=True)

    class Meta:
        model = PersonAddress
        exclude = ['person']
        autofill = {
            'country': ['select', 1, 'CDNX_ext_location_country_foreign'],
            'region': ['select', 1, 'CDNX_ext_location_regions_foreign', 'country'],
            'province': ['select', 1, 'CDNX_ext_location_provinces_foreign', 'region'],
            'city': ['select', 1, 'CDNX_ext_location_citys_foreign', 'country', 'region', 'province'],
        }

    def __groups__(self):
        g = [
            (_('PersonAddress'), 12,
                ['alias', 6],
                ['main_delivery', 3],
                ['main_invoice', 3],
                ['country', 6],
                ['region', 6, None, None, None, None, None, ["ng-change=reset_fields(['province', 'city'])"]],
                ['province', 6, None, None, None, None, None, ["ng-change=reset_fields(['city'])"]],
                ['city', 6],
                ['town', 6],
                ['zipcode', 6],
                ['address', 12],
                ['mobile_phone', 6],
                ['phone', 6],),
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('PersonAddress'), 12,
                ['alias', 6],
                ['main_delivery', 6],
                ['main_invoice', 6],
                ['country', 6],
                ['region', 6],
                ['province', 6],
                ['city', 6],
                ['town', 6],
                ['zipcode', 6],
                ['address', 6],
                ['mobile_phone', 6],
                ['phone', 6],),
        ]
        return g


class CompanyForm(GenModelForm):

    class Meta:
        model = Company
        exclude = ['storage', 'pos', 'storage_contacts']

    def __groups__(self):
        return [
            (
                _('Details'), 12,
                ['person', 9],
                ['active', 3],
            ),
        ]

    @staticmethod
    def __groups_details__():
        return [
            (
                _('Details'), 12,
                ['person', 9],
                ['active', 3],
            ),
        ]


class PublicistForm(GenModelForm):
    class Meta:
        model = Publicist
        exclude = []

    def __groups__(self):
        return [
            (
                _('Details'), 12,
                ['person', 9],
                ['enable', 3],
            )
        ]

    @staticmethod
    def __groups_details__():
        return [
            (
                _('Details'), 12,
                ['person', 9],
                ['enable', 3],
            )
        ]


class AuthorshipForm(GenModelForm):
    class Meta:
        model = Authorship
        exclude = ['author', ]

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['person', 6],
            )
        ]
        return g
