# -*- coding: utf-8 -*-
import uuid
import math

from django.db.models import F, Q, Max, Min, Avg
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import gettext as _

from django.conf import settings

from codenerix_products.models import Family, Category
from codenerix_products.models import ProductFinal, Subcategory
from codenerix_payments.models import PaymentRequest, Currency, PaymentError
from codenerix_invoicing.models import BillingSeries
from codenerix_invoicing.models_sales import Customer
from codenerix_email.models import EmailTemplate, EmailMessage
from codenerix_pos.models import POS

from erp.people.models import Person


def DynamicLanguageModel(nameModel, baseModel, modelConection):
    listModel = []
    for lang in settings.LANGUAGES:
        # Con esto me aseguro de que solo 1 de los idiomas es obligatorio.
        null = "True"
        if lang[0] == settings.LANGUAGES[0][0]:
            null = "False"

        lang_code = lang[0].upper()
        query = ("class {}Text{}({}):\n").format(nameModel, lang_code, baseModel)
        query += (
            "  {}= models.OneToOneField({}, blank=False, null=False, related_name='{}')\n"
        ).format(modelConection, nameModel, lang_code)
        query += (
            "  name = models.CharField(_('Name {}'), max_length=150, blank={}, null={})\n"
        ).format(lang_code, null, null)
        listModel.append(query)

    return listModel


def DynamicLanguageImport(path, name, form=False):
    if not form:
        string = "from {} import {}Text{}\n"
    else:
        string = "from {} import {}TextForm{}\n"

    listImport = []
    for lang in settings.LANGUAGES:
        query = string.format(path, name, lang[0].upper())
        listImport.append(query)
    return listImport


def get_POS(request):
    # Decide UUID
    uuid_pos = request.session.get("POS_client_UUID", None)
    if uuid_pos:
        pos = POS.objects.filter(uuid=uuid_pos).first()
    else:
        pos = None
        request.session["POS_client_UUID"] = None

    # Decide COMMIT
    commit = request.session.get("POS_client_COMMIT", None)
    if not commit:
        commit = None
        request.session["POS_client_COMMIT"] = None

    # Decide POS
    if pos:
        return {"uuid": str(pos.uuid), "POS": pos, "commit": commit}
    else:
        return {"uuid": "", "POS": None, "commit": commit}


def get_menu(lang):
    menu = {}
    families = (
        Family.objects.filter(public=True, show_menu=True)
        .annotate(slug=F("{}__slug".format(lang)), name=F("{}__name".format(lang)))
        .values("pk", "slug", "name", "icon")
        .order_by("order", "name")
    )
    menu["families"] = list(families)

    categories = (
        Category.objects.filter(public=True)
        .annotate(
            slug=F("{}__slug".format(lang)),
            slug_family=F("family__{}__slug".format(lang)),
            name=F("{}__name".format(lang)),
        )
        .values("pk", "slug", "name", "slug_family")
        .order_by("order", "name")
    )
    menu["categories"] = categories
    return menu
    """
    menu = {}
    order_cat = []
    for option in ProductFinal.objects.filter(
        product__category__show_menu=True,
        product__category__public=True,
        product__subcategory__show_menu=True,
        product__subcategory__public=True,
        product__brand__outstanding=True,
        product__brand__show_menu=True
    ).values(
        'product__category__pk',
        'product__category__{}__name'.format(lang),
        'product__category__{}__slug'.format(lang),
        'product__subcategory__pk',
        'product__subcategory__{}__name'.format(lang),
        'product__subcategory__{}__slug'.format(lang),
        'product__subcategory__show_brand',
        'product__brand__pk',
        'product__brand__{}__name'.format(lang),
        'product__brand__{}__slug'.format(lang)
    ).order_by(
        'product__category__order',
        'product__subcategory__order',
        'product__brand__order'
    ).distinct():
        cat_pk = option['product__category__pk']
        subcat_pk = option['product__subcategory__pk']
        if cat_pk not in order_cat:
            order_cat.append(cat_pk)

        if cat_pk not in menu:
            menu[cat_pk] = {
                'id': cat_pk,
                'label': option['product__category__{}__name'.format(lang)],
                'slug': option['product__category__{}__slug'.format(lang)],
                'subcategories': {},
                'subcategories_order': []
            }
        if subcat_pk not in menu[cat_pk]['subcategories']:
            info_subcat = {
                'id': subcat_pk,
                'label': option['product__subcategory__{}__name'.format(lang)],
                # 'slug': u"{}/{}".format(option['product__category__{}__slug'.format(lang)], option['product__subcategory__{}__slug'.format(lang)]),
                'slug': u"{}".format(option['product__subcategory__{}__slug'.format(lang)]),
                'brands': []
            }
            menu[cat_pk]['subcategories_order'].append(subcat_pk)
            menu[cat_pk]['subcategories'][subcat_pk] = info_subcat

        if option['product__subcategory__show_brand']:
            menu[cat_pk]['subcategories'][subcat_pk]['brands'].append({
                'label': option['product__brand__{}__name'.format(lang)],
                'slug': u"{}/{}".format(option['product__subcategory__{}__slug'.format(lang)], option['product__brand__{}__slug'.format(lang)]),
            })

    menu_order = []

    for cat in order_cat:
        info_cat = menu[cat].copy()
        info_cat['subcategories'] = []
        info_cat.pop('subcategories_order')
        for sub in menu[cat]['subcategories_order']:
            info_cat['subcategories'].append(menu[cat]['subcategories'][sub])

        " ""
        Si la categoria solo tiene una categoria publica, se redirige hacia ella
        " ""
        if Subcategory.objects.filter(
            category=cat, public=True
        ).count() == 1:
            info_cat['slug'] = info_cat['subcategories'][0]['slug']
        menu_order.append(info_cat)

    return menu_order
    """


class PaymentMethod(object):
    def get_currency(self):
        currency_id = "EUR"
        cs = Currency.objects.filter(iso4217=currency_id)
        context = {
            "error": False,
            "error_code": "",
            "error_message": "",
            "currency": None,
        }

        if len(cs) == 0:
            c = Currency()
            c.name = "Euro"  # "Dollar"
            c.symbol = "€".decode("utf-8")  # "$"
            c.iso4217 = currency_id
            c.price = 1.0  # 1.14
            c.save()
            context["currency"] = c
        elif len(cs) == 1:
            context["currency"] = cs[0]
        else:
            context["error"] = True
            context["error_code"] = "C001"
            context["error_message"] = "Currency {} found more than once".format(
                currency_id
            )
        return context

    def pay(self, payment_method, url_reverse, total, shopping_cart):
        """
        payment_method => key de settings.PAYMENTS
        url_reverse => related name de la url de vuelta por parte del banco
        total => cantidad total a pagar
        shopping_cart => shopping_cart asociado
        """
        context = {
            "error": False,
            "error_code": "",
            "error_message": "",
            "payment_request": None,
            "btn": None,
        }
        if not hasattr(settings, "PAYMENTS") and not settings.PAYMENTS:
            context["error"] = True
            context["error_code"] = "P001"
            context["error_message"] = _(
                "Payment Request: ERROR - faltan parametros de configuracion"
            )
        elif "meta" not in settings.PAYMENTS.keys() and not settings.PAYMENTS["meta"]:
            context["error"] = True
            context["error_code"] = "P002"
            context["error_message"] = _(
                "Payment Request: ERROR - configuracion erronea"
            )
        elif (
            "real" not in settings.PAYMENTS["meta"].keys()
            and not settings.PAYMENTS["meta"]["real"]
        ):
            context["error"] = True
            context["error_code"] = "P003"
            context["error_message"] = _(
                "Payment Request: ERROR - estructura de configuracion erronea"
            )
        else:
            currency = self.get_currency()
            if currency["error"]:
                context["error"] = True
                context["error_code"] = currency["error_code"]
                context["error_message"] = currency["error_message"]
            else:
                pr = PaymentRequest()
                pr.reverse = url_reverse
                pr.currency = currency["currency"]
                pr.platform = payment_method
                pr.real = settings.PAYMENTS["meta"]["real"]
                pr.total = math.ceil(float(total) * 100) / 100.0
                pr.order = shopping_cart.pk
                try:
                    pr.save()
                    shopping_cart.payment.add(pr)
                    context["payment_request"] = pr
                except PaymentError as e:
                    context["error"] = True
                    context["error_code"] = "P004"
                    context["error_message"] = _("Payment Request: ERROR - (e)") % {
                        "e": e
                    }

                if not context["error"]:
                    try:
                        context["btn"] = pr.get_approval()
                    except NoReverseMatch as e:
                        context["error"] = True
                        context["error_code"] = "P005"
                        context["error_message"] = _("Payment Request: ERROR - (e)") % {
                            "e": e
                        }

        return context


def create_user(first_name, last_name, email, password, lang):

    # Check if this email address is already in use
    user = User.objects.filter(username=email).first()

    # If no user found with that email address
    if user is None:
        if password is None:
            password = uuid.uuid4().hex

        # Create the user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()

        # Create person
        person = Person(user=user, name=first_name, surname=last_name, lang=lang)
        person.save()

        # Create customer
        customer = Customer(
            billing_series=BillingSeries.objects.get(default=True), external=person
        )
        customer.save()

        # Set the customer to this person
        person.customer = customer
        person.save()

        # Prepare context
        context = {
            "username": email,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
        }

        # Prepare for sending the email
        send_email("ALTAUSER01", lang, context, user.email)

        # Return the just created user
        return (user, password)

    else:
        # Email address already in use
        raise ValueError("Email address already registered")


def send_email_admins(subject, body):

    # Add extra information to the email
    subject = "[{}] {}".format(settings.INFO_PROJECT["name_project"], subject)
    body += """
--
{name_project} Helper v{version}
""".format(
        version=settings.VERSION, name_project=settings.INFO_PROJECT["name_project"]
    )

    # For each ADMIN
    for eto in settings.ADMINS:
        email = EmailMessage()
        email.subject = subject
        email.body = body
        email.eto = eto[1]
        email.efrom = settings.DEFAULT_FROM_EMAIL
        email.sending = True
        email.save()
        email.send(legacy=True)


def send_email(cid, lang, context, email, now=False):

    # Get the email with the given template
    email_message = EmailTemplate.get(cid=cid, lang=lang, context=context)

    # If we found it
    if email_message:
        # Set the destination and save
        email_message.eto = email
        if now:
            email_message.sending = True
            email_message.save()
            email_message.send()
        else:
            email_message.save()
    else:
        # If not found the template, send an error
        subject = "[{}] Intento fallido de envio de email {}".format(
            settings.INFO_PROJECT["name_project"], cid
        )
        body = """
Hola,

Se ha intentado enviar un email con la siguiente información:

\tcid: {cid} \t\t(CID no encontrado en base de datos!!!!)
\temail: {email}
\tlang: {lang}
\tcontext: {context}

Un saludo,
""".format(
            cid=cid, email=email, lang=lang, context=context
        )
        send_email_admins(subject, body)
