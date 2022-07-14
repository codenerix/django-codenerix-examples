# -*- coding: utf-8 -*-
import hashlib
import random
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.forms.utils import ErrorList
from django.views.generic import FormView

from codenerix.views import (
    GenList,
    GenCreate,
    GenCreateModal,
    GenUpdate,
    GenUpdateModal,
    GenDelete,
    GenDetail,
    GenDetailModal,
    GenForeignKey,
)

# from codenerix_extensions.helpers import get_language_database
from codenerix_extensions.files.views import DocumentFileView
from codenerix_extensions.helpers import get_language_database
from codenerix_invoicing.models import BillingSeries
from codenerix_invoicing.models_sales import Customer, CustomerDocument, Address
from codenerix_invoicing.forms_sales import CustomerDocumentForm
from codenerix_invoicing.views_sales import (
    GenCustomerDocumentUrl,
    CustomerDocumentDetailsModal,
    CustomerDocumentUpdateModal,
    CustomerDocumentDelete,
)
from codenerix_products.models import TypeTax, Product
from codenerix_pos.models import POSHardware, KIND_POSHARDWARE_DNIE
from codenerix_geodata.models import Country, Province

from erp.common.helpers import get_menu

# ESTO ESTABA COMENTADO, he comentado el codigo dependiente porque hay vistas que lo usan y
# PYFLAKES me genera avisos todo el tiempo, si no debe estar aquí borra lo demás también
from django.utils.translation import get_language
from erp.common.helpers import create_user

from .models import (
    Person,
    PersonAddress,
    Company,
    Publicist,
    Authorship,
)  # , PersonDependent
from .forms import (
    PersonForm,
    PersonAddressForm,
    CustomerRegisterForm,
    LoginForm,
    CompanyForm,
    PublicistForm,
    AuthorshipForm,
    PersonFormOnly,
    PersonFormForService,
)  # , PersonDependentForm, PersonDependentFormModal


class GenProfile(object):
    ws_entry_point = "people/profiles"


class Profile(GenProfile, GenList):
    model = Person
    linkadd = False
    show_details = True
    extra_context = {"status": "profile"}
    extends_base = "frontend/backend_user.html"
    permission_group = "Customer"
    # template_model = "people/profile_list.html"
    onlybase = True
    static_app_row = "people/js/profile_app"

    def __limitQ__(self, info):
        limit = {}
        limit["file_link"] = Q(user=info.user)
        return limit

    def dispatch(self, *args, **kwargs):
        lang = get_language_database()
        self.extra_context["menu"] = get_menu(lang)
        return super(Profile, self).dispatch(*args, **kwargs)


class ProfileDetails(GenProfile, GenDetail):
    model = Person
    groups = PersonFormOnly.__groups_details__()
    # template_model = "people/profile_details.html"
    linkback = False
    linkdelete = False
    exclude_fields = [
        "customer",
        "user",
        "creator",
        "lang",
        "pos_operator",
        "provider",
        "disabled",
    ]
    permission_group = "Customer"

    tabs = [
        {
            "id": "lines",
            "name": _("Address"),
            "ws": "customer_personaddress_sublist_frontend",
            "rows": "base",
        },
        {
            "id": "Documents",
            "name": _("Documents"),
            "ws": "persondocuments_sublist",
            "rows": "base",
        },
    ]

    def get_object(self):
        queryset = self.model.objects.filter(user__pk=self.request.user.pk)
        if queryset:
            pk = queryset.first().pk
        else:
            pk = 0
        return get_object_or_404(queryset, pk=pk)


class ProfileUpdate(GenProfile, GenUpdate):
    model = Person
    form_class = PersonFormOnly
    show_details = True
    linkdelete = False
    linksavenew = False
    linksavehere = False
    permission_group = "Customer"

    def get_object(self):
        queryset = self.model.objects.filter(user__pk=self.request.user.pk)
        if queryset:
            pk = queryset.first().pk
        else:
            pk = 0
        return get_object_or_404(queryset, pk=pk)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileUpdate, self).get_context_data(**kwargs)
        context["form"].fields["email"].initial = self.request.user.email
        return context

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            self.request.user.email = email
            self.request.user.username = email
            self.request.user.save()
        except IntegrityError as error:
            errors = form._errors.setdefault("email", ErrorList())
            errors.append(_("Email already exists!"))
            return self.form_invalid(form)
        return super(ProfileUpdate, self).form_valid(form)


class CustomerRegister(FormView):
    # template_model = 'people/register.html'
    template_model = "registration/login_frontend.html"
    template_name = "registration/login_frontend.html"

    success_url = reverse_lazy("home")
    form_class = CustomerRegisterForm
    form_class_login = LoginForm
    form_class_register = CustomerRegisterForm
    model = User

    def dispatch(self, *args, **kwargs):
        self.success_url = self.request.GET.get("next", self.success_url)
        return super(CustomerRegister, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {}
        lang = get_language_database()
        context["user"] = getattr(request, "user", None)
        context["menu"] = get_menu(lang)
        #        context['menu'] = get_menu(get_language_database())
        context["form"] = self.form_class_login
        context["form2"] = self.form_class_register

        return render(self.request, self.template_model, context)

    def post(self, request, *args, **kwargs):
        # En el caso que el html haya sido tocado, no se continuará por ninguna vía, simplemente se recarga la página.
        self.way = 0

        # Si me viene en el campo hiden un registes_form, el usuario se está registrando.
        if "login_form" in request.POST:
            self.way = 1
            self.form_class = self.form_class_login

            return super(CustomerRegister, self).post(request, *args, **kwargs)

        # En caso contrario es un login.
        elif "register_form" in request.POST:
            self.way = 2
            self.form_class = self.form_class_register
            return super(CustomerRegister, self).post(request, *args, **kwargs)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.way == 1:
            context["form"] = form
            context["form2"] = self.form_class_register
        elif self.way == 2:
            context["form"] = self.form_class_login
            context["form2"] = form
        context["way"] = self.way
        return self.render_to_response(context)

    def form_valid(self, form):
        if self.way == 1:
            # Recollect data
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Check if the user exists
            user = authenticate(username=username, password=password)

            # If the user exists, check that is active and it gave us the right password
            if user:
                # El usuario se puede registrar o bien siendo superuser o bien siendo customer.
                if (
                    user.is_active
                    and hasattr(user, "person")
                    and hasattr(user.person, "customer")
                    and user.person.customer is not None
                ) or user.is_superuser:

                    login(self.request, user)
                else:
                    # User is not active
                    raise ValidationError(_("The user must be a active costumer"))
            else:
                # User is not active or the password did'nt match
                raise ValidationError(_("Wrong user or password"))

            return super(CustomerRegister, self).form_valid(form)

        # Si es un registro tomo este otro.
        elif self.way == 2:
            # recovery element
            name = form.cleaned_data["name"]
            surname = form.cleaned_data["surname"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            address = form.cleaned_data["address"]
            country = form.cleaned_data["country"]
            province = form.cleaned_data["province"]
            town = form.cleaned_data["town"]
            zipcode = form.cleaned_data["zipcode"]
            phone = form.cleaned_data["phone"]

            billing = BillingSeries.objects.filter(default=True).first()

            if billing:
                # open transaction save.
                with transaction.atomic():
                    lang = get_language()

                    user, password = create_user(
                        first_name=name,
                        last_name=surname,
                        email=email,
                        password=password,
                        lang=lang,
                    )

                    person_address = PersonAddress()
                    person_address.person = user.person
                    person_address.address = address
                    person_address.country = Country.objects.filter(pk=country).first()
                    person_address.province = Province.objects.filter(
                        code=province
                    ).first()
                    person_address.town = town
                    person_address.zipcode = zipcode
                    person_address.phone = phone
                    person_address.save()

                    user = authenticate(username=email, password=password)
                    login(self.request, user)

                    # TODO: Falta enviar un email al cliente notificandole su nuevo registro

            return super(CustomerRegister, self).form_valid(form)


# PERSONS
class PersonList(GenList):
    model = Person
    extra_context = {
        "menu": ["manager", "people"],
        "bread": [_("Manager"), _("People")],
    }


class PersonCreate(GenCreate):
    model = Person
    form_class = PersonForm

    def get_form_class(self, *args, **kwargs):
        # Get the form
        form_class = super(PersonCreate, self).get_form_class(*args, **kwargs)
        # clean cache
        if "readonly" in form_class.base_fields["username"].widget.attrs:
            del form_class.base_fields["username"].widget.attrs["readonly"]

        # Set the in_user Meta
        form_class.Meta.in_user = None

        # Return form
        return form_class

    def form_valid(self, form):
        # Get fields
        username = form.cleaned_data.get("username", None)
        password = form.cleaned_data.get("password", None)
        confirm = form.cleaned_data.get("confirm", None)
        email = form.cleaned_data.get("email", None)

        try:
            with transaction.atomic():
                # Presave if required
                if username and password and email and confirm:
                    form.instance.presave(username, password, email, confirm)

                # Let the class finish it works
                return super(PersonCreate, self).form_valid(form)
        except ValidationError as error:
            errors = form._errors.setdefault("nid", ErrorList())
            errors.append(error)
            return self.form_invalid(form)


class PersonCreateModal(GenCreateModal, PersonCreate):
    pass


class PersonUpdate(GenUpdate):
    model = Person
    form_class = PersonForm
    linkdelete = False

    def get_form_class(self, *args, **kwargs):
        # Get the form
        form_class = super(PersonUpdate, self).get_form_class(*args, **kwargs)
        # Set the in_user Meta
        form_class.Meta.in_user = self.object.user

        # field username readonly
        if self.object.user:
            form_class.base_fields["username"].widget.attrs["readonly"] = True
            if self.object.user.is_staff:
                raise Http404

        # If user exists, exclude username field
        if form_class.Meta.in_user:
            if "exclude_fields" in dir(form_class.Meta):
                form_class.Meta.exclude_fields.append("username")
            else:
                form_class.Meta.exclude_fields = ["username"]

        # Return new form
        return form_class

    def form_valid(self, form):
        # Prepare fields
        # cannot modify username
        if self.object.user:
            username = self.object.user.username
        else:
            username = form.cleaned_data.get("username", None)
        password = form.cleaned_data.get("password", None)
        confirm = form.cleaned_data.get("confirm", None)
        email = form.cleaned_data.get("email", None)

        try:
            with transaction.atomic():
                # Presave if required
                if (confirm and password) or email:
                    form.instance.presave(username, password, email, confirm)

                # Let the class finish it works
                return super(PersonUpdate, self).form_valid(form)
        except ValidationError as error:
            errors = form._errors.setdefault("nid", ErrorList())
            errors.append(error)
            return self.form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(PersonUpdate, self).get_context_data(**kwargs)
        person = context["person"]
        if person.user:
            context["form"].fields["email"].initial = person.user.email
            context["form"].fields["username"].initial = person.user.username
        return context


class PersonUpdateModal(GenUpdateModal, PersonUpdate):
    pass


class PersonDelete(GenDelete):
    model = Person


class PersonForeign(GenForeignKey):
    model = Person
    label = "{name} {surname}"

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        qsobject = Q(nid__icontains=search)
        qsobject |= Q(name__icontains=search)
        qsobject |= Q(surname__icontains=search)
        qs = queryset.filter(qsobject)

        return qs[: settings.LIMIT_FOREIGNKEY]


class PersonAuthorStaticPageForeign(GenForeignKey):
    model = Person
    label = "{name} {surname}"

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        qsobject = Q(nid__icontains=search)
        qsobject |= Q(name__icontains=search)
        qsobject |= Q(surname__icontains=search)
        qs = queryset.filter(qsobject)

        return qs[: settings.LIMIT_FOREIGNKEY]


# PersonAddress
# -------------------Sublist customer---
class CustomerPersonAddressSubList(GenList):
    model = PersonAddress

    def __limitQ__(self, info):
        # raise Exception("_")
        limit = {}
        limit["file_link"] = Q(person__pk=info.user.person.pk)
        return limit

    def __fields__(self, info):
        fields = []
        # fields.append(('person', _('Person')))
        fields.append(("alias", _("Alias")))
        fields.append(("country", _("Country")))
        fields.append(("region", _("Region")))
        fields.append(("province", _("Province")))
        fields.append(("city", _("City")))
        # fields.append(('zipcode', _("Postal code")))
        fields.append(("address", _("Address")))
        # fields.append(('phone', _("Phone")))
        fields.append(("main_invoice", _("Main invoice")))
        fields.append(("main_delivery", _("Main delivery")))
        return fields


class CustomerPersonAddressSubListBackend(CustomerPersonAddressSubList):
    def __limitQ__(self, info):
        limit = {}
        return limit


class CustomerPersonAddressCreateModal(GenCreateModal):
    model = PersonAddress
    form_class = PersonAddressForm
    hide_foreignkey_button = True

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__user_pk = self.request.user.pk
        return super(CustomerPersonAddressCreateModal, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__user_pk:
            person = Person.objects.get(user__pk=self.__user_pk)
            self.request.person = person
            form.instance.person = person

        return super(CustomerPersonAddressCreateModal, self).form_valid(form)


class CustomerPersonAddressUpdateModal(GenUpdateModal, GenUpdate):
    model = PersonAddress
    form_class = PersonAddressForm
    hide_foreignkey_button = True


class CustomerPersonAddressSubDelete(GenDelete):
    model = PersonAddress


class CustomerPersonAddressDetailsModal(GenDetailModal):
    model = PersonAddress
    groups = PersonAddressForm.__groups_details__()
    exclude_fields = ["person"]


# -------------------Sublist provider---
class ProviderPersonAddressSubList(GenList):
    model = PersonAddress
    # show_details = True
    # json = False
    # template_model = "people/provider_personaddress_sublist.html"

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get("pk", None)
        limit["file_link"] = Q(person__provider__pk=pk)
        return limit


class ProviderPersonAddressCreateModal(GenCreateModal):
    model = PersonAddress
    form_class = PersonAddressForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__providers_pk = kwargs.get("pk", None)
        return super(ProviderPersonAddressCreateModal, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__providers_pk:
            person = Person.objects.get(provider__pk=self.__providers_pk)
            self.request.person = person
            form.instance.person = person

        return super(ProviderPersonAddressCreateModal, self).form_valid(form)


class ProviderPersonAddressUpdateModal(GenUpdateModal):
    model = PersonAddress
    form_class = PersonAddressForm


class ProviderPersonAddressSubDelete(GenDelete):
    model = PersonAddress


class ProviderPersonAddressDetailsModal(GenDetailModal):
    model = PersonAddress
    groups = PersonAddressForm.__groups_details__()

    exclude_fields = ["person"]


class CompanyList(GenList):
    model = Company


class CompanyCreate(GenCreate):
    model = Company
    form_class = CompanyForm


class CompanyCreateModal(GenCreateModal, CompanyCreate):
    pass


class CompanyUpdate(GenUpdate):
    model = Company
    form_class = CompanyForm


class CompanyUpdateModal(GenUpdateModal, CompanyUpdate):
    pass


class CompanyDelete(GenDelete):
    model = Company


class CompanyForeign(GenForeignKey):
    model = Company
    label = "{person__name} {person__surname}"

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        qsobject = Q(person__nid__icontains=search)
        qsobject |= Q(person__name__icontains=search)
        qsobject |= Q(person__surname__icontains=search)
        qs = queryset.filter(qsobject)

        return qs[: settings.LIMIT_FOREIGNKEY]


# ###############################
class PersonDocumentSubList(GenCustomerDocumentUrl, GenList):
    model = CustomerDocument

    def __fields__(self, info):
        fields = []
        fields.append(("type_document", _("Type document")))
        fields.append(("name_file", _("Name file")))

        return fields

    def __limitQ__(self, info):
        limit = {}
        limit["file_link"] = Q(customer__external__user__pk=info.user.pk)
        return limit


class PersonDocumentCreateModal(
    GenCustomerDocumentUrl, DocumentFileView, GenCreateModal, GenCreate
):
    model = CustomerDocument
    form_class = CustomerDocumentForm
    hide_foreignkey_button = True

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__user_pk = self.request.user.pk
        return super(PersonDocumentCreateModal, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if self.__user_pk:
            customer = Customer.objects.get(external__pk=self.__user_pk)
            self.request.customer = customer
            form.instance.customer = customer

        return super(PersonDocumentCreateModal, self).form_valid(form)


class PersonDocumentDetailsModal(CustomerDocumentDetailsModal):
    pass


class PersonDocumentUpdateModal(CustomerDocumentUpdateModal):
    hide_foreignkey_button = True


class PersonDocumentDelete(CustomerDocumentDelete):
    pass


class ServicePersonCreateModal(GenCreateModal, GenCreate):
    model = Person
    form_class = PersonFormForService

    def get_form_class(self, *args, **kwargs):
        # Get the form
        form_class = super(ServicePersonCreateModal, self).get_form_class(
            *args, **kwargs
        )
        form_class.Meta.in_user = None

        # Set the subscription system
        uuid = self.request.session.get("POS_client_UUID", None)
        poshw = POSHardware.objects.filter(
            pos__uuid=uuid, kind=KIND_POSHARDWARE_DNIE, enable=True
        ).first()
        if uuid and poshw:
            uid = poshw.uuid.hex
            form_class.Meta.subscriptions = {
                uid: {
                    "name": ["firstname"],
                    "surname": ["lastname"],
                    "nid": ["cid"],
                    "nid_type": [
                        "kind",
                        {
                            "mapper": "return value=='DNIE' && 'D' || 'U'",
                            "default": "U",
                        },
                    ],
                },
            }

        # Return form
        return form_class

    def form_valid(self, form):
        # Get fields
        email = form.cleaned_data.get("email", None)
        nid = form.cleaned_data.get("nid", None)
        nid_type = form.cleaned_data.get("nid_type", None)

        error = Person.validate_nid(nid, nid_type)
        if error:
            errors = form._errors.setdefault("nid", ErrorList())
            errors.append(error)
            return self.form_invalid(form)

        try:
            with transaction.atomic():
                # Presave if required
                if email:
                    username = email
                    password = hashlib.md5(
                        "{}cwjHditJ{}VaARLxChe{}WdSSVUIvYt{}".format(
                            int(random.random() * random.randrange(1, 1000)),
                            int(random.random() * random.randrange(1, 1000)),
                            int(random.random() * random.randrange(1, 1000)),
                            int(random.random() * random.randrange(1, 1000)),
                        )
                    ).hexdigest()
                    confirm = password
                    form.instance.presave(username, password, email, confirm)

                # Let the class finish it works
                return super(ServicePersonCreateModal, self).form_valid(form)
        except ValidationError as error:
            errors = form._errors.setdefault("nid", ErrorList())
            errors.append(error)
            return self.form_invalid(form)


class ServicePersonUpdate(GenUpdate):
    model = Person
    form_class = PersonFormForService
    linkdelete = False

    def get_form_class(self, *args, **kwargs):
        # Get the form
        form_class = super(ServicePersonUpdate, self).get_form_class(*args, **kwargs)
        # Set the in_user Meta
        form_class.Meta.in_user = self.object.user
        return form_class

    def form_valid(self, form):
        # Prepare fields
        # cannot modify username
        if self.object.user:
            email = self.object.user.email
        else:
            email = form.cleaned_data.get("email", None)

        try:
            with transaction.atomic():
                # Presave if required
                if email:
                    username = email
                    password = hashlib.md5(
                        "{}0g8W5mmmMIaRA{}ivWhzfVyE9Bi2{}BoaiXXr1gAk76{}".format(
                            int(random.random() * random.randrange(1, 1000)),
                            int(random.random() * random.randrange(1, 1000)),
                            int(random.random() * random.randrange(1, 1000)),
                            int(random.random() * random.randrange(1, 1000)),
                        )
                    ).hexdigest()
                    confirm = password
                    form.instance.presave(username, password, email, confirm)

                # Let the class finish it works
                return super(ServicePersonUpdate, self).form_valid(form)
        except ValidationError as error:
            errors = form._errors.setdefault("nid", ErrorList())
            errors.append(error)
            return self.form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ServicePersonUpdate, self).get_context_data(**kwargs)
        person = context["person"]
        if person.user:
            context["form"].fields["email"].initial = person.user.email
        return context


# ############################
# Reception
class PublicistList(GenList):
    model = Publicist
    extra_context = {
        "menu": ["publicist", "people"],
        "bread": [_("Publicist"), _("People")],
    }


class PublicistCreate(GenCreate):
    model = Publicist
    form_class = PublicistForm

    def form_valid(self, form):
        person = form.cleaned_data.get("person", None)
        if person is None or person.user is None:
            errors = form._errors.setdefault("person", ErrorList())
            errors.append(
                _(
                    "You can not refresh permissions for a Person wich doesn't have an associated user"
                )
            )
            return super(PublicistCreate, self).form_invalid(form)
        else:
            return super(PublicistCreate, self).form_valid(form)


class PublicistCreateModal(GenCreateModal, PublicistCreate):
    pass


class PublicistUpdate(GenUpdate):
    model = Publicist
    form_class = PublicistForm

    def form_valid(self, form):
        person = form.cleaned_data.get("person", None)
        if person is None or person.user is None:
            errors = form._errors.setdefault("person", ErrorList())
            errors.append(
                _(
                    "You can not refresh permissions for a Person wich doesn't have an associated user"
                )
            )
            return super(PublicistUpdate, self).form_invalid(form)
        else:
            return super(PublicistUpdate, self).form_valid(form)


class PublicistUpdateModal(GenUpdateModal, PublicistUpdate):
    pass


class PublicistDelete(GenDelete):
    model = Publicist


class PublicistSubList(GenList):
    model = Publicist
    show_details = False
    json = False
    template_model = "billings/people_sublist.html"
    extra_context = {
        "menu": ["Reception", "people"],
        "bread": [_("Reception"), _("People")],
    }

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get("pk", None)
        limit["link"] = Q(xxxxxxx__pk=pk)
        return limit


class PublicistDetails(GenDetail):
    model = Publicist
    groups = PublicistForm.__groups_details__()


class PublicistDetailModal(GenDetailModal, PublicistDetails):
    pass


# ###########################################
# Authorship
class AuthorshipList(GenList):
    model = Authorship
    extra_context = {
        "menu": ["Authorship", "people"],
        "bread": [_("Authorship"), _("People")],
    }


class AuthorshipCreate(GenCreate):
    model = Authorship
    form_class = AuthorshipForm


class AuthorshipCreateModal(GenCreateModal, AuthorshipCreate):
    pass


class AuthorshipUpdate(GenUpdate):
    model = Authorship
    form_class = AuthorshipForm


class AuthorshipUpdateModal(GenUpdateModal, AuthorshipUpdate):
    pass


class AuthorshipDelete(GenDelete):
    model = Authorship


# PersonAddressForeign
class PersonAddressForeignDelivery(GenForeignKey):
    model = Address
    label = "{name} {surname}"

    def build_label(self, obj):
        address = ""
        if obj.external_delivery.city:
            address = "{} ".format(obj.external_delivery.city)
        if obj.external_delivery.town:
            address += "{}".format(obj.external_delivery.town)

        if address != "":
            address += ". "

        if obj.external_delivery.address:
            address += "{}".format(obj.external_delivery.address)

        if obj.external_delivery.address and obj.external_delivery.zipcode:
            address += ", {}".format(
                obj.external_delivery.address, obj.external_delivery.zipcode
            )
        elif obj.external_delivery.zipcode:
            address += "{}".format(obj.external_delivery.zipcode)

        if obj.external_delivery.phone and obj.external_delivery.mobile_phone:
            address += " {} / {}".format(
                obj.external_delivery.phone, obj.external_delivery.mobile_phone
            )
        if obj.external_delivery.phone:
            address += " {}".format(obj.external_delivery.phone)
        if obj.external_delivery.mobile_phone:
            address += " {}".format(obj.external_delivery.mobile_phone)

        return address

    def get_foreign(self, queryset, search, filters):
        lang = get_language_database()

        # Filter with search string
        qsobject = Q(external_delivery__town__icontains=search)
        qsobject |= Q(
            **{"external_delivery__city__{}__name__icontains".format(lang): search}
        )
        qsobject |= Q(external_delivery__address__icontains=search)
        qsobject |= Q(external_delivery__zipcode__icontains=search)
        qsobject |= Q(external_delivery__phone__icontains=search)
        qsobject |= Q(external_delivery__mobile_phone__icontains=search)
        qs = queryset.filter(qsobject)

        customer_pk = filters.get("customer", None)
        if customer_pk:
            qs = qs.filter(external_delivery__person__customer__pk=customer_pk)

        return qs


class PersonAddressForeignInvoice(GenForeignKey):
    model = Address
    label = "{name} {surname}"

    def build_label(self, obj):
        address = ""
        if obj.external_invoice.city:
            address = "{} ".format(obj.external_invoice.city)
        if obj.external_invoice.town:
            address += "{}".format(obj.external_invoice.town)

        if address != "":
            address += ". "

        if obj.external_invoice.address:
            address += "{}".format(obj.external_invoice.address)

        if obj.external_invoice.address and obj.external_invoice.zipcode:
            address += ", {}".format(
                obj.external_invoice.address, obj.external_invoice.zipcode
            )
        elif obj.external_invoice.zipcode:
            address += "{}".format(obj.external_invoice.zipcode)

        if obj.external_invoice.phone and obj.external_invoice.mobile_phone:
            address += " {} / {}".format(
                obj.external_invoice.phone, obj.external_invoice.mobile_phone
            )
        if obj.external_invoice.phone:
            address += " {}".format(obj.external_invoice.phone)
        if obj.external_invoice.mobile_phone:
            address += " {}".format(obj.external_invoice.mobile_phone)

        return address

    def get_foreign(self, queryset, search, filters):
        lang = get_language_database()

        # Filter with search string
        qsobject = Q(external_invoice__town__icontains=search)
        qsobject |= Q(
            **{"external_invoice__city__{}__name__icontains".format(lang): search}
        )
        qsobject |= Q(external_invoice__address__icontains=search)
        qsobject |= Q(external_invoice__zipcode__icontains=search)
        qsobject |= Q(external_invoice__phone__icontains=search)
        qsobject |= Q(external_invoice__mobile_phone__icontains=search)
        qs = queryset.filter(qsobject)

        customer_pk = filters.get("customer", None)
        if customer_pk:
            qs = qs.filter(external_invoice__person__customer__pk=customer_pk)

        return qs
