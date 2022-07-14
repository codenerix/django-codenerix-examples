# -*- coding: utf-8 -*-
import ast
import datetime
import math
import json
import time
import uuid

from math import ceil
from os.path import join
from operator import or_
from functools import reduce
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import F, Q, Max, Min, Avg, Sum
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template import Context, Template, TemplateDoesNotExist
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _, get_language
from django.views.generic import View

from codenerix_extensions.helpers import get_language_database

# from codenerix.lib.genmail import EmailMessage, get_connection
from codenerix_email.models import EmailMessage

from codenerix.views import GenList, GenUpdate, GenDetail, GenCreate, GenDelete

from codenerix_products.models import (
    FlagshipProduct,
    Product,
    ProductFinalImage,
    ProductFinal,
    ProductImage,
    ProductDocument,
    ProductFeature,
    ProductFinalAttribute,
    Family,
    Category,
    Subcategory,
    Brand,
    TYPE_VALUE_LIST,
    TYPE_VALUE_BOOLEAN,
    TYPE_VALUE_FREE,
    OptionValueFeature,
    OptionValueAttribute,
)

from codenerix_cms.models import Slider, StaticPage, CHOICE_PUBLIC

# from codenerix_invoicing.models_sales import SalesOrder, SalesLineOrder, SalesInvoice, SalesBasket, SalesLineBasket, ROLE_BASKET_BUDGET, ROLE_BASKET_SHOPPINGCART, ROLE_BASKET_WISHLIST, SalesLineInvoice, SalesOrderDocument
# from codenerix_invoicing.models_sales import SalesOrder, SalesLines__________staticmethod as SalesLineOrder, SalesInvoice, SalesBasket, SalesLines__________staticmethod as SalesLineBasket, ROLE_BASKET_BUDGET, ROLE_BASKET_SHOPPINGCART, ROLE_BASKET_WISHLIST, SalesLines__________staticmethod as SalesLineInvoice, SalesLines__________staticmethod as SalesOrderDocument
# from codenerix_invoicing.forms_sales import InvoiceForm, BasketForm, LineBasketForm
# from codenerix_invoicing.forms_sales import BasketForm
from codenerix_invoicing.helpers import ShoppingCartProxy

# from codenerix_reviews.models import Reviews
from codenerix.helpers import form_answer

from codenerix_geodata.models import Country, Region, Province, City

from codenerix_payments.models import PaymentRequest

from erp.common.helpers import get_menu, PaymentMethod, create_user
from erp.people.models import PersonAddress
from erp.people.forms import get_country, get_provinces
from erp.common.helpers import send_email, send_email_admins
from erp.transports.views import TransportCalculate
from erp.frontend.forms import OrderForm, RequestInvoiceForm

imp = []
for lang_code in settings.LANGUAGES_DATABASES:
    imp.append("ProductFinalText{}".format(lang_code))
exec("from codenerix_products.models import {}".format(",".join(imp)))


def frontend(request, filename):
    try:
        return render(request, "frontend/{}".format(filename))
    except TemplateDoesNotExist:
        raise Http404()


@login_required
def not_authorized(request):
    return render(request, "frontend/not_authorized.html")


# Mixins
class TranslatedMixin(object):
    @property
    def lang(self):
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code == self.request.LANGUAGE_CODE:
                return self.request.LANGUAGE_CODE.lower()
        return settings.LANGUAGES[0][0].lower()


# ######
class GenBudget(object):
    ws_entry_point = "backend/budgets"


class BudgetList(GenBudget, GenList):
    pass


"""
class BudgetList(GenBudget, GenList):
    model = SalesBasket
    show_details = True
    default_ordering = '-date'
    extra_context = {
        'status': 'shopping_cart'
    }
    extends_base = "frontend/backend_user.html"

    def __limitQ__(self, info):
        limit = {}
        limit['role'] = Q(role=ROLE_BASKET_BUDGET)
        # limits['user'] = Q(customer__external__user=info.user)
        # limits['public'] = Q(public=True)
        return limit

    def get_context_data(self, **kwargs):
        lang = get_language_database()
        self.extra_context['menu'] = get_menu(lang)
        context = super(BudgetList, self).get_context_data(**kwargs)

        return context
"""


class BudgetDetails(GenBudget, GenDetail):
    pass


"""
class BudgetDetails(GenBudget, GenDetail):
    model = SalesBasket
    groups = BasketForm.__groups_details__()

    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_saleslinebaskets_sublist', 'rows': 'base'},
    ]
"""


class BudgetUpdate(GenBudget, GenUpdate):
    pass


"""
class BudgetUpdate(GenBudget, GenUpdate):
    model = SalesBasket
    show_details = True
    form_class = BasketForm
"""


class GenOrder(object):
    ws_entry_point = "backend/orders"


class OrderList(GenOrder, GenList):
    pass


"""
class OrderList(GenOrder, GenList):
    model = SalesOrder
    show_details = True
    default_ordering = '-date'
    extra_context = {
        'status': 'orders'
    }
    gentrans = {
        'Requestinvoice': _("Request invocie"),
    }

    extends_base = "frontend/backend_user.html"
    linkadd = False
    linkdelete = False
    template_model = 'frontend/order_list.html'
    static_partial_row = 'frontend/partials/order_row.html'

    def __limitQ__(self, info):
        limit = {}
        limit['user'] = Q(customer__external__user=info.user)
        return limit

    def dispatch(self, *args, **kwargs):
        lang = get_language_database()
        self.extra_context['menu'] = get_menu(lang)
        return super(OrderList, self).dispatch(*args, **kwargs)

    def __fields__(self, info):
        fields = []
        # fields.append(('customer', _('Customer')))
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        # fields.append(('storage', _('Storage')))
        fields.append(('get_status_order_display', _('Status')))
        fields.append(('status_order', None))
        # fields.append(('payment_detail', _('Payment detail')))
        # fields.append(('source', _('Source of purchase')))
        fields.append((None, _('Invoices')))
        return fields

    def json_builder(self, answer, context):
        body = self.bodybuilder(context['object_list'], self.autorules())
        orders = []
        for order in body:
            temp = order.copy()
            temp['documents'] = list(SalesOrderDocument.objects.filter(order__pk=temp['pk'], kind__code='FACTURACLIENTE').values('doc_path', 'name_file'))

            orders.append(temp)

        answer['table']['body'] = orders
        return answer
"""


class OrderDetails(GenOrder, GenDetail):
    pass


"""
class OrderDetails(GenOrder, GenDetail):
    model = SalesOrder
    groups = OrderForm.__groups_details__()
    linkedit = False
    linkdelete = False
    exclude_fields = ['parent_pk', 'customer', 'budget', 'billing_series', 'storage', 'payment_detail', 'payment', 'source', 'number_tracking', 'lock', ]
    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'front_lineordersaless_sublist', 'rows': 'base'},
    ]
"""


class LineOrderSubList(GenList):
    pass


"""
class LineOrderSubList(GenList):
    model = SalesLineOrder
    linkadd = False
    linkedit = False

    def __fields__(self, info):
        fields = []
        fields.append(('quantity', _("Quantity")))
        fields.append(('description', _("Description")))
        fields.append(('price_base', _("Price base")))
        fields.append(('discount', _("Discount (%)")))
        fields.append(('discounts', _("Total Discount")))
        fields.append(('tax', _("Tax (%)")))
        # fields.append(('equivalence_surcharge', _("Equivalence surcharge (%)")))
        fields.append(('taxes', _("Total Tax")))
        fields.append(('total', _("Total")))
        return fields

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(order__pk=pk)
        return limit

    def get_context_dataxx(self, **kwargs):
        context = super(LineOrderSubList, self).get_context_data(**kwargs)
        order_pk = self.kwargs.get('pk', None)
        if order_pk:
            order = SalesOrder.objects.get(pk=order_pk)
            context['total'] = order.calculate_price_doc()
        else:
            context['total'] = 0
        return context

"""


class RequestInvoice(View):
    template_model = "frontend/requestinvoice_formmodal.html"
    form_class = RequestInvoiceForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RequestInvoice, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Context
        context = {}

        user = request.user

        ini = {
            "name": user.person.name,
            "surname": user.person.surname,
            "nid": user.person.nid,
            "nid_type": user.person.nid_type,
        }
        form = self.form_class(initial=ini)
        form.Meta.name = _("Datos para la facturación")

        context["form"] = form
        context["cannot_update"] = False

        return render(self.request, self.template_model, context)

    def post(self, request, *args, **kwargs):
        # Get parameters
        try:
            query = json.loads(request._body.decode("utf-8"))
        except Exception:
            query = {}

        answer = {
            "error": None,
            "error_code": None,
        }

        order_pk = kwargs.get("orderk", None)

        if order_pk and query:
            name = query.get("name", None)
            surname = query.get("surname", None)
            nid = query.get("nid", None)
            nid_type = query.get("nid_type", None)

            order = SalesOrder.objects.filter(
                pk=order_pk, customer__external__user=getattr(request, "user", None)
            ).first()
            if order:
                # enviar email a los adminitradores con el CID 'RequestInvoice'
                # devolver mensaje al usuario de 'factura solicitada, en breve estará disponible en su panel'
                user = request.user
                context = {
                    "customer": order.customer,
                    "order": order,
                    # datos traidos desde el formulario
                    "new_name": name,
                    "new_surname": surname,
                    "new_nid": nid,
                    "new_nid_type": nid_type,
                    # datos guardados en bbdd
                    "name": user.person.name,
                    "surname": user.person.surname,
                    "nid": user.person.nid,
                    "nid_type": user.person.nid_type,
                }
                if order.budget.address_invoice:
                    # direccion de facturacion
                    context["address"] = (
                        order.budget.address_invoice.external_invoice.get_address(),
                    )
                    context["zipcode"] = (
                        order.budget.address_invoice.external_invoice.get_zipcode(),
                    )
                    context["city"] = (
                        order.budget.address_invoice.external_invoice.get_city(),
                    )
                    context["province"] = (
                        order.budget.address_invoice.external_invoice.get_province(),
                    )
                    context["country"] = (
                        order.budget.address_invoice.external_invoice.get_country(),
                    )
                else:
                    context["address"] = ""
                    context["zipcode"] = ""
                    context["city"] = ""
                    context["province"] = ""
                    context["country"] = ""

                for email in settings.CLIENTS:
                    send_email("SOLICITUDFACTURA", get_language(), context, email[1])

                answer["message"] = _(
                    "Factura solicitada, en breve estará disponible en su area personal"
                )
            else:
                # error, pedido no encontrado
                answer["error_code"] = "E02"
                answer["error"] = _("Order not found!")
        else:
            # error, parametros incorrectos
            answer["error_code"] = "E01"
            answer["error"] = _("Invalid parameters")

        if answer["error_code"]:
            emails_admin = []
            for (name, email) in settings.ADMINS:
                emails_admin.append(email)

            error_debug = request.__dict__
            if settings.DEBUG:
                legacy = False
            else:
                legacy = True
            for email in emails_admin:
                email_message = EmailMessage()
                email_message.efrom = settings.DEFAULT_FROM_EMAIL
                email_message.eto = email
                email_message.subject = "[{}] {}".format(
                    settings.INFO_PROJECT["name_project"], _(" Request Invoice")
                )
                email_message.body = "Hello:\n\nThere was an exception while using RequestInvoice, code: {error_code}, there is some problem :\n\n{error_message}\n\n{error_debug}\n\nThank you,\n\n--{name_project} Helper v({version})".format(
                    error_code=answer["error_code"],
                    error_message=answer["error"],
                    error_debug=error_debug,
                    version=settings.VERSION,
                    name_project=settings.INFO_PROJECT["name_project"],
                )
                email_message.save()
                email_message.send(legacy=legacy, silent=True)

        return form_answer("accept", answer)


# ######
class GenWishList(object):
    ws_entry_point = "backend/wishlists"


class WishListList(GenWishList, GenList):
    pass


"""
class WishListList(GenWishList, GenList):
    model = SalesBasket
    show_details = True
    default_ordering = '-updated'
    extra_context = {
        'status': 'wishlist'
    }
    extends_base = "frontend/backend_user.html"

    def __limitQ__(self, info):
        limit = {}
        limit['role'] = Q(role=ROLE_BASKET_WISHLIST)
        # limits['user'] = Q(customer__external__user=info.user)
        return limit

    def get_context_data(self, **kwargs):
        lang = get_language_database()
        self.extra_context['menu'] = get_menu(lang)
        context = super(WishListList, self).get_context_data(**kwargs)

        return context
"""


class WishListDetails(GenWishList, GenDetail):
    pass


"""
class WishListDetails(GenWishList, GenDetail):
    model = SalesBasket
    groups = BasketForm.__groups_details__()

    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_saleslinebaskets_sublist', 'rows': 'base'},
    ]

    def get_context_data(self, **kwargs):
        lang = get_language_database()
        self.extra_context['menu'] = get_menu(lang)
        context = super(WishListDetails, self).get_context_data(**kwargs)

        return context
"""


class WishListUpdate(GenWishList, GenUpdate):
    pass


"""
class WishListUpdate(GenWishList, GenUpdate):
    model = SalesBasket
    show_details = True
    form_class = BasketForm
"""


class WishListProductList(GenList):
    pass


"""
class WishListProductList(GenList):
    model = SalesLineBasket

    template_model = 'frontend/wishlistproduct_list.html'
    static_partial_row = 'frontend/partials/wishlistproduct_row.html'

    default_ordering = '-updated'
    ws_entry_point = 'backend/wishlistproducts'
    extra_context = {
        'status': 'wishlistproduct'
    }

    linkadd = False
    show_details = False
    field_check = False
    field_delete = True

    ngincludes = {
        'table': '/static/frontend/partials/table_wishlistproduct.html'
    }
    gentrans = {
        'Buy': _('Buy'),
    }

    def __limitQ__(self, info):
        limit = {}
        limit['user'] = Q(basket__customer__external__user=info.user)
        limit['removed'] = Q(removed=False)
        return limit

    def __fields__(self, info):
        lang = get_language_database()
        return (
            ('product__{}__name'.format(lang), _('Product'), 100),
            ('quantity', _('Quantity'), 100),
            ('slug:product__{}__slug'.format(lang), '', 100),
        )

    def get_context_data(self, **kwargs):
        lang = get_language_database()
        self.extra_context['menu'] = get_menu(lang)
        context = super(WishListProductList, self).get_context_data(**kwargs)

        return context
"""


class WishListProductCreate(GenCreate):
    pass


"""
class WishListProductCreate(GenCreate):
    model = SalesLineBasket
    form_class = LineBasketForm
    ws_entry_point = "backend/wishlistproducts"

    def get_form_kwargs(self):
        kwargs = super(WishListProductCreate, self).get_form_kwargs()

        customer = self.request.user.person.customer

        try:
            wishlist = SalesBasket.objects.get(customer=customer, role=ROLE_BASKET_WISHLIST)
        except ObjectDoesNotExist:
            wishlist = SalesBasket(customer=customer, name=_("Default"), role=ROLE_BASKET_WISHLIST)
            wishlist.save()

        kwargs['data']['wish_list'] = wishlist.pk

        return kwargs

"""


class WishListProductDelete(GenDelete):
    pass


"""
class WishListProductDelete(GenDelete):
    model = SalesLineBasket
    ws_entry_point = "backend/wishlistproducts"
"""


class WishListProductBuy(View):
    pass


"""
class WishListProductBuy(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        customer = request.user.person.customer

        try:
            cart = SalesBasket.objects.filter(customer=customer, role=ROLE_BASKET_SHOPPINGCART)
        except ObjectDoesNotExist:
            cart = SalesBasket(customer=customer, name=_('Default'), role=ROLE_BASKET_SHOPPINGCART)
            cart.save()

        wishlistproducts_pks = [int(pk) for pk in ast.literal_eval(request._body)['lines']]
        for wishlist_product in SalesLineBasket.objects.filter(pk__in=wishlistproducts_pks):
            try:
                cart_line = cart.line_basket_sales.get(Q(product__pk=wishlist_product.product_final.pk))
                cart_line.quantity += wishlist_product.quantity
                cart_line.save()
            except ObjectDoesNotExist:
                cart_line = SalesLineBasket(
                    basket=cart,
                    product=wishlist_product.product_final,
                    quantity=wishlist_product.quantity
                )
            cart_line.save()
            wishlist_product.delete()

        return JsonResponse({
            'url': reverse_lazy('shopping_cart')
        })
"""


class GenInvoice(object):
    ws_entry_point = "backend/invoices"


class InvoiceList(GenInvoice, GenList):
    pass


"""
class InvoiceList(GenInvoice, GenList):
    model = SalesInvoice
    show_details = True
    default_ordering = '-date'
    extra_context = {
        'status': 'invoices'
    }
    extends_base = "frontend/backend_user.html"
    linkadd = False

    def dispatch(self, *args, **kwargs):
        lang = get_language_database()
        self.extra_context['menu'] = get_menu(lang)
        return super(InvoiceList, self).dispatch(*args, **kwargs)

    def __limitQ__(self, info):
        limit = {}
        limit['user'] = Q(customer__external__user=info.user)
        return limit

    def __fields__(self, info):
        fields = []
        # fields.append(('customer', _('Customer')))
        fields.append(('code', _('Code')))
        fields.append(('date', _('Date')))
        # fields.append(('tax', _('Tax')))
        return fields

"""


class InvoiceDetails(GenInvoice, GenDetail):
    pass


"""
class InvoiceDetails(GenInvoice, GenDetail):
    model = SalesInvoice
    groups = InvoiceForm.__groups_details__()
    linkedit = False
    linkdelete = False
    exclude_fields = ['parent_pk', 'lock', ]

    tabs = [
        {'id': 'lines', 'name': _('Products'), 'ws': 'CDNX_invoicing_saleslinebaskets_sublist', 'rows': 'base'},
    ]
"""


class GenSlugLevelGet(TranslatedMixin, View):
    template_name = "frontend/index.html"

    @property
    def apply_surcharge(self):
        raise Exception(_("Function deprecated!"))

    # obtenemos las marcas, categorias y subcategorias donde hay productos que cumplen la query
    def search_products(self, query, lang):
        categories = {}
        brands = []
        range_price = [None, None]
        # temporaly
        list_categories = []
        list_subcategories = {}
        list_brands = []

        filters = [
            "{}__name__icontains".format(lang),
            "{}__slug__icontains".format(lang),
            "code__icontains",
            "product__code__icontains",
            "product__model__icontains",
            "product__{}__name__icontains".format(lang),
            "product__{}__slug__icontains".format(lang),
            "product__brand__{}__name__icontains".format(lang),
            "product__brand__{}__slug__icontains".format(lang),
            "product__family__{}__name__icontains".format(lang),
            "product__family__{}__slug__icontains".format(lang),
            "product__category__{}__name__icontains".format(lang),
            "product__category__{}__slug__icontains".format(lang),
            "product__subcategory__{}__name__icontains".format(lang),
            "product__subcategory__{}__slug__icontains".format(lang),
        ]

        queryset_custom = None
        for filter_txt in filters:
            queryset_custom_and = None
            for word in query.split():
                if queryset_custom_and:
                    queryset_custom_and &= Q(**{filter_txt: word})
                else:
                    queryset_custom_and = Q(**{filter_txt: word})
            if queryset_custom:
                queryset_custom |= queryset_custom_and
            else:
                queryset_custom = queryset_custom_and

        queryset = (
            ProductFinal.objects.filter(
                Q(product__products_image__principal=True),
                queryset_custom,
                product__public=True,
            )
            .annotate(
                product_name=F("product__{}__name".format(lang)),
                product_slug=F("product__{}__slug".format(lang)),
                product_brand_name=F("product__brand__{}__name".format(lang)),
                product_brand_slug=F("product__brand__{}__slug".format(lang)),
                product_category_name=F("product__category__{}__name".format(lang)),
                product_category_slug=F("product__category__{}__slug".format(lang)),
                product_subcategory_name=F(
                    "product__subcategory__{}__name".format(lang)
                ),
                product_subcategory_slug=F(
                    "product__subcategory__{}__slug".format(lang)
                ),
                name=F("{}__name".format(lang)),
                slug=F("{}__slug".format(lang)),
            )
            .order_by("product__brand__{}__name".format(lang))
        )

        for product in queryset:
            # category
            if product.product.category.pk not in list_categories:
                list_categories.append(product.product.category.pk)
                categories[product.product.category.pk] = {
                    "label": product.product_category_name,
                    "subcategories": [],
                }
                list_subcategories[product.product.category.pk] = []
            # subcategory
            if (
                product.product.subcategory
                and product.product.subcategory.pk
                not in list_subcategories[product.product.category.pk]
            ):
                categories[product.product.category.pk]["subcategories"].append(
                    {
                        "val": product.product.subcategory.pk,
                        "label": product.product_subcategory_name,
                    }
                )
                list_subcategories[product.product.category.pk].append(
                    product.product.subcategory.pk
                )
            # brand
            if product.product.brand and product.product.brand.pk not in list_brands:
                list_brands.append(product.product.brand.pk)
                brands.append(
                    {
                        "pk": product.product.brand.pk,
                        "slug": product.product_brand_slug,
                        "name": product.product_brand_name,
                        "image": product.product.brand.image,
                        "outstanding": product.product.brand.outstanding,
                    }
                )
            # range price
            # min
            if range_price[0] is None or range_price[0] > product.price:
                range_price[0] = int(math.floor(product.price))
            # max
            if range_price[1] is None or range_price[1] < product.price:
                range_price[1] = int(math.ceil(product.price))

            if range_price[0] is None:
                range_price[0] = 0.0

            if range_price[1] is None:
                range_price[1] = 0.0

        return brands, categories, range_price

    def find_product_final(self, lang, queryset):
        """
        find a product final enabled
        """
        return ProductFinal.find_product(queryset, lang, onlypublic=True)

    def find_product(self, lang, queryset):
        """
        find a product enabled
        """
        return Product.find_product(queryset, lang, onlypublic=True)

    def find_subcategory(self, lang, slug_subcategory, slug_category=None):
        """
        find a subcategory enabled
        """
        if slug_category:
            queryset = []
            for langs in settings.LANGUAGES:
                queryset.append(
                    Q(
                        **{
                            "{}__slug".format(langs[0].lower()): slug_subcategory,
                            "category__{}__slug".format(
                                langs[0].lower()
                            ): slug_category,
                        }
                    )
                )
        else:
            queryset = self.get_qs(slug_subcategory)

        return (
            Subcategory.objects.filter(reduce(or_, queryset), public=True)
            .values(
                "pk",
                "code",
                "image",
                "{}__name".format(lang),
                "{}__slug".format(lang),
                "{}__description".format(lang),
                "category__pk".format(lang),
                "category__{}__name".format(lang),
                "category__{}__slug".format(lang),
                "category__family__{}__slug".format(lang),
                "category__image".format(lang),
                "category__family__image".format(lang),
                "category__family__icon".format(lang),
            )
            .annotate(
                name=F("{}__name".format(lang)),
                slug=F("{}__slug".format(lang)),
                # category=F("category__{}__name".format(lang)),
                category_slug=F("category__{}__slug".format(lang)),
                family_slug=F("category__family__{}__slug".format(lang)),
                description=F("{}__description".format(lang)),
                meta_title=F("{}__meta_title".format(lang)),
                meta_description=F("{}__meta_description".format(lang)),
                meta_keywords=F("{}__meta_keywords".format(lang)),
            )
            .first()
        )

    def find_family(self, lang, slug_family):
        """
        find a family enabled
        """
        # queryset = self.get_qs(slug_family)
        family = (
            Family.objects.filter(
                **{
                    # reduce(or_, queryset)
                    "public": True,
                    "{}__slug".format(lang): slug_family,
                }
            )
            .values(
                "pk",
                "code",
                "image",
                "icon",
                "{}__name".format(lang),
                "{}__slug".format(lang),
                "{}__description".format(lang),
            )
            .annotate(
                name=F("{}__name".format(lang)),
                slug=F("{}__slug".format(lang)),
                description=F("{}__description".format(lang)),
                meta_title=F("{}__meta_title".format(lang)),
                meta_description=F("{}__meta_description".format(lang)),
                meta_keywords=F("{}__meta_keywords".format(lang)),
            )
            .first()
        )
        return family

    def find_category(self, lang, slug_category):
        """
        find a subcategory enabled
        """
        queryset = self.get_qs(slug_category)
        return (
            Category.objects.filter(reduce(or_, queryset), public=True)
            .values(
                "pk",
                "code",
                "image",
                "{}__name".format(lang),
                "{}__slug".format(lang),
                "family__{}__slug".format(lang),
                "family__image".format(lang),
                "family__icon".format(lang),
                "{}__description".format(lang),
            )
            .annotate(
                name=F("{}__name".format(lang)),
                slug=F("{}__slug".format(lang)),
                description=F("{}__description".format(lang)),
                slug_family=F("family__{}__slug".format(lang)),
                meta_title=F("{}__meta_title".format(lang)),
                meta_description=F("{}__meta_description".format(lang)),
                meta_keywords=F("{}__meta_keywords".format(lang)),
            )
            .first()
        )

    def find_brand(self, slug_brand):
        """
        find a brand enabled
        """
        result = (
            Brand.objects.filter(
                Q(**{"{}__slug__icontains".format(self.lang): slug_brand}), public=True
            )
            .values("pk", "{}__name".format(self.lang), "{}__slug".format(self.lang))
            .annotate(
                name=F("{}__name".format(self.lang)),
                slug=F("{}__slug".format(self.lang)),
            )
            .first()
        )
        if result:
            result.pop("{}__name".format(self.lang))
            result.pop("{}__slug".format(self.lang))
        return result

    def find_staticpage(self, lang, slug):
        """
        find a static page enabled
        """
        queryset = self.get_qs(slug)
        answer = (
            StaticPage.objects.filter(status=CHOICE_PUBLIC)
            .filter(reduce(or_, queryset))
            .values(
                "{}__tiles".format(lang),
                "template__template".format(lang),
            )
            .annotate(
                tiles=F("{}__tiles".format(lang)),
            )
            .first()
        )
        return answer

    def context_basic(self, request, lang):
        context = {}
        context["user"] = getattr(request, "user", None)
        context["menu"] = get_menu(lang)
        return context

    def is_subcategory(self, lang, context, subcategory):
        """
        info for the subcategory
        """
        self.template_name = "frontend/subcategoria.html"
        context["url"] = reverse_lazy(
            "list_products_frontend", kwargs={"type": "SUB", "pk": subcategory["pk"]}
        )
        if subcategory["image"] == "":
            if subcategory["category__image"] != "":
                head_image = subcategory["category__image"]
            elif subcategory["category__family__image"] != "":
                head_image = subcategory["category__family__image"]
            else:
                head_image = None
        else:
            head_image = subcategory["image"]

        context["head_image"] = head_image
        context["icon_image"] = subcategory["category__family__icon"]
        context["subcategory"] = subcategory

        context["meta_title"] = subcategory["meta_title"]
        context["meta_description"] = subcategory["meta_description"]
        context["meta_keywords"] = subcategory["meta_keywords"]
        # Slug
        context["title"] = (subcategory["slug"], subcategory["name"])
        home_url = reverse_lazy("home")
        category_url = join(home_url, subcategory["category_slug"])
        subcategory_url = join(category_url, subcategory["slug"])
        context["menu"]["subcategories"] = self.get_subcategory(
            lang, category=subcategory["category__pk"], show_all=True
        )
        # raise Exception(self.get_subcategory(lang, category=subcategory['category__pk'], show_all=True))
        # context['products'] = self.get_products(lang, subcategory_pk=subcategory['pk'])
        context["slugs"] = [
            (home_url, _("Home")),
            (category_url, subcategory["category"]),
            (subcategory_url, subcategory["name"]),
        ]
        context["select"] = (subcategory["family_slug"], subcategory["category_slug"])
        return context

    def __get_attributes(selt, product_final):
        text = []
        for pfa in ProductFinalAttribute.objects.filter(product=product_final).order_by(
            "attribute__order"
        ):
            if pfa.attribute.type_value == TYPE_VALUE_LIST:
                lang = get_language_database()
                field = "{}__description".format(lang)
                ov = (
                    OptionValueAttribute.objects.filter(
                        group=pfa.attribute.list_value, pk=int(pfa.value)
                    )
                    .values(field)
                    .first()
                )
                if ov:
                    text.append(ov[field])
        return " ".join(text)

    def is_product(self, lang, context, product):
        """
        info for the product
        """
        self.template_name = "frontend/{}.html".format("producto")

        if product["subcategory_image"] != "":
            head_image = product["subcategory_image"]
        elif product["category_image"] != "":
            head_image = product["category_image"]
        elif product["family_image"] != "":
            head_image = product["family_image"]
        else:
            head_image = ""
        context["head_image"] = head_image
        context["icon_image"] = product["family__icon"]

        context["meta_title"] = product["meta_title"]
        context["meta_description"] = product["meta_description"]
        context["meta_keywords"] = product["meta_keywords"]

        context["product"] = product
        product_finals = {}
        menu_products_final = {}
        for product_final in ProductFinal.objects.filter(product__pk=product["pk"]):
            if product_final.weight:
                if product_final.weight < 1000:
                    peso = product_final.weight
                    unidad = "g"
                else:
                    peso = product_final.weight / 1000
                    unidad = "Kg"
                # tiene decimales
                if abs(peso) - abs(int(peso)) == 0:
                    formato = "{0:.0f} {1}"
                else:
                    formato = "{0:.2f} {1}"
                weight = formato.format(peso, unidad)
            else:
                weight = ""

            product_finals[product_final.pk] = {
                "code": product_final.code,
                "info": ProductFinal.find_product(
                    [
                        Q(pk=product_final.pk),
                    ],
                    lang,
                ),
                "weight": weight,
                "name": getattr(getattr(product_final.product, lang, {}), "name", ""),
                "attributes": self.__get_attributes(product_final),
                "images": ProductFinalImage.objects.filter(
                    product_final=product_final,
                    public=True,
                )
                .values("image", "{}__description".format(lang))
                .annotate(
                    description=F("{}__description".format(lang)),
                )
                .order_by("-principal", "order"),
            }
            menu_products_final[product_final.pk] = {
                "slug": product_finals[product_final.pk]["info"]["slug"],
                "label": product_finals[product_final.pk]["attributes"],
            }

        context["product_finals"] = product_finals

        context["images"] = (
            ProductImage.objects.filter(product=product["pk"], public=True)
            .values("image", "{}__description".format(lang))
            .annotate(
                description=F("{}__description".format(lang)),
            )
            .order_by("order")
        )

        context["documents"] = (
            ProductDocument.objects.filter(product=product["pk"], public=True)
            .values("name_file", "doc_path", "{}__description".format(lang))
            .annotate(
                description=F("{}__description".format(lang)),
            )
        )

        context["menu"]["subcategories"] = self.get_subcategory(
            lang, category=product["category__pk"], show_all=True
        )
        context["menu"]["products"] = self.get_products(
            lang, subcategory_pk=product["subcategory__pk"]
        )
        if len(menu_products_final) > 1:
            context["menu"]["products_final"] = menu_products_final
        # Slug
        context["title"] = (product["slug"], product["name"])
        context["slugs"] = [
            (reverse_lazy("home"), _("Home")),
            (product["category_slug"], product["category_name"]),
            (product["subcategory_slug"], product["subcategory_name"]),
        ]
        context["select"] = (
            product["family_slug"],
            product["category_slug"],
            product["subcategory_slug"],
            product["slug"],
        )

        if self.request.user.is_authenticated() and hasattr(
            self.request.user, "person"
        ):
            # Adds if the user can review or not this product
            customer = self.request.user.person.customer

            orders_pks = (
                SalesOrder.objects.filter(customer=customer, status_order="DE")
                .only("pk")
                .values_list("pk", flat=True)
            )  # Delivered orders to the current client

            product_pk = context["product"]["pk"]
            """
            if SalesLineOrder.objects.filter(
                Q(product__pk=product_pk),
                order__in=orders_pks,
            ).exists():  # If the customer already buyed the product
                context['can_review'] = not Reviews.objects.filter(
                    Q(product__pk=product_pk),
                    customer=customer
                ).exists()
            else:
                context['can_review'] = False
            """
        else:
            context["can_review"] = False

        return context

    def is_product_final(self, lang, context, product):
        """
        info for the product
        """
        self.template_name = "frontend/{}.html".format("producto_final")
        if not product["description_short"]:
            product["description_short"] = product["product_description_short"]
        product.pop("product_description_short")
        if not product["description_long"]:
            product["description_long"] = product["product_description_long"]
        product.pop("product_description_long")
        if not product["meta_title"]:
            product["meta_title"] = product["product_meta_title"]
        product.pop("product_meta_title")
        if not product["meta_description"]:
            product["meta_description"] = product["product_meta_description"]
        product.pop("product_meta_description")

        product.pop("product__family__{}__slug".format(lang))
        product.pop("product__family__{}__description".format(lang))
        product.pop("product__category__code".format(lang))
        product.pop("product__category__image".format(lang))
        product.pop("product__category__{}__slug".format(lang))
        product.pop("product__category__{}__name".format(lang))
        product.pop("product__category__{}__description".format(lang))
        product.pop("product__subcategory__{}__slug".format(lang))
        product.pop("product__subcategory__{}__name".format(lang))
        product.pop("product__subcategory__{}__description".format(lang))
        product.pop("{}__meta_title".format(lang))
        product.pop("{}__meta_description".format(lang))
        product.pop("{}__description_short".format(lang))
        product.pop("{}__description_long".format(lang))
        product.pop("{}__slug".format(lang))
        product.pop("{}__name".format(lang))
        product.pop("product__{}__meta_title".format(lang))
        product.pop("product__{}__meta_description".format(lang))
        product.pop("product__{}__description_short".format(lang))
        product.pop("product__{}__description_long".format(lang))

        if product["subcategory_image"] != "":
            head_image = product["subcategory_image"]
        elif product["category_image"] != "":
            head_image = product["category_image"]
        elif product["family_image"] != "":
            head_image = product["family_image"]
        else:
            head_image = ""
        context["head_image"] = head_image
        context["icon_image"] = product["family_icon"]

        context["meta_title"] = product["meta_title"]
        context["meta_description"] = product["meta_description"]
        context["meta_keywords"] = product["meta_keywords"]

        context["product"] = product
        context["images"] = (
            ProductFinalImage.objects.filter(product_final=product["pk"], public=True)
            .values("image", "{}__description".format(lang))
            .annotate(
                description=F("{}__description".format(lang)),
            )
            .order_by("-principal", "order")
        )
        context["documents"] = (
            ProductDocument.objects.filter(product=product["product__pk"], public=True)
            .values("name_file", "doc_path", "{}__description".format(lang))
            .annotate(
                description=F("{}__description".format(lang)),
            )
        )
        context["features"] = (
            ProductFeature.objects.filter(product=product["product__pk"])
            .values(
                "value",
                "feature__type_value",
                "feature__image",
                "feature__{}__description".format(lang),
            )
            .annotate(
                description=F("feature__{}__description".format(lang)),
            )
        )
        context["attributes"] = (
            ProductFinalAttribute.objects.filter(product=product["pk"])
            .values(
                "value", "attribute__image", "attribute__{}__description".format(lang)
            )
            .annotate(
                description=F("attribute__{}__description".format(lang)),
            )
        )
        context["select"] = (
            product["family_slug"],
            product["category_slug"],
            product["subcategory_slug"],
            product["slug"],
        )

        context["products_related"] = []
        for prod in (
            ProductFinal.objects.filter(
                productsrelated=product["pk"], product__products_image__principal=True
            )
            .values(
                "{}__slug".format(lang),
                "offer",
                "created",
                "offer",
                "pk",
                "product__{}__name".format(lang),
                "product__model",
                "product__brand__{}__name".format(lang),
                "product__products_image__image",
                "{}__meta_title".format(lang),
            )
            .distinct()
        ):
            prod["slug"] = prod["{}__slug".format(lang)]
            prod["meta_title"] = prod["{}__meta_title".format(lang)]
            prod["image"] = prod["product__products_image__image"]
            prod["name"] = prod["product__{}__name".format(lang)]
            prod["brand"] = prod["product__brand__{}__name".format(lang)]
            prod["new"] = (
                1
                if (timezone.now() - product["created"]).days
                <= settings.CDNX_PRODUCTS_NOVELTY_DAYS
                else 0
            )
            # si es menor a 5 dias es nuevo
            prod.pop("{}__slug".format(lang))
            prod.pop("{}__meta_title".format(lang))
            prod.pop("product__products_image__image")
            prod.pop("product__{}__name".format(lang))
            prod.pop("product__brand__{}__name".format(lang))
            prod.pop("created")

            context["products_related"].append(prod)
        # Saco todas los comentarios validos del producto en el lenguaje del usuario.
        reviews_qs = Reviews.objects.filter(
            product=product["pk"], validate=True, lang=lang
        ).only("customer__external__name", "stars", "reviews", "created", "updated")

        context["reviews"] = reviews_qs.values(
            "customer__external__name", "stars", "reviews", "created", "updated"
        ).annotate(customer_name=F("customer__external__name"))
        for review in context["reviews"]:
            review.pop("customer__external__name")

        if reviews_qs.count():
            context["product"]["stars"] = int(
                round(reviews_qs.aggregate(Avg("stars")).values()[0])
            )
        else:
            context["product"]["stars"] = 0

        # Slug
        context["title"] = (product["slug"], product["name"])
        context["slugs"] = [
            (reverse_lazy("home"), _("Home")),
            (product["category_slug"], product["category_name"]),
            (product["subcategory_slug"], product["subcategory_name"]),
        ]

        if self.request.user.is_authenticated() and hasattr(
            self.request.user, "person"
        ):
            # Adds if the user can review or not this product
            customer = self.request.user.person.customer

            orders_pks = (
                SalesOrder.objects.filter(customer=customer, status_order="DE")
                .only("pk")
                .values_list("pk", flat=True)
            )  # Delivered orders to the current client

            product_pk = context["product"]["pk"]
            if SalesLineOrder.objects.filter(
                Q(product__pk=product_pk),
                order__in=orders_pks,
            ).exists():  # If the customer already buyed the product
                context["can_review"] = not Reviews.objects.filter(
                    Q(product__pk=product_pk), customer=customer
                ).exists()
            else:
                context["can_review"] = False
        else:
            context["can_review"] = False

        return context

    def is_staticpage(self, lang, context, staticpage):
        """
        info for the static page
        """
        self.html_response = """{{% extends "frontend/base_shop.html" %}}
                                {{% load cdnxcms_tiler_validator %}}
                                {{% load cdnxcms_tiler %}}
                                {{% block contenido %}}
                                {}
                                {{% endblock %}}""".format(
            staticpage["template__template"]
        )
        context.update(staticpage)
        return context

    def is_brand(self, lang, context, brand):
        """
        info for the brand
        """
        context["brand"] = brand
        # Slug
        context["title"] = (brand["slug"], brand["name"])
        context["slugs"] = [
            (reverse_lazy("home"), _("Home")),
            (brand["slug"], brand["name"]),
        ]
        self.template_name = "frontend/{}.html".format("subcategoria")
        return context

    def is_family(self, lang, context, family):
        self.template_name = "frontend/{}.html".format("family")
        # Slug
        context["family"] = family
        context["title"] = (family["slug"], family["name"])

        context["head_image"] = family["image"]
        context["icon_image"] = family["icon"]

        context["meta_title"] = family["meta_title"]
        context["meta_description"] = family["meta_description"]
        context["meta_keywords"] = family["meta_keywords"]

        # context['subcategories'] = self.get_category(lang, family=family['pk'], show_all=True)
        # context['outstanding'] = self.get_outstanding_product(lang, family=family['pk'])
        # context['recommended'] = self.get_recommended_product(lang, family=family['pk'])
        # context['products'] = self.get_products(lang, family_pk=family['pk'])
        context["categories"] = self.get_categories(lang, family_pk=family["pk"])
        context["slugs"] = [
            (reverse_lazy("home"), _("Home")),
            (family["slug"], family["name"]),
        ]
        context["select"] = (family["slug"], "")

        return context

    def is_category(self, lang, context, category):
        self.template_name = "frontend/{}.html".format("categoria")
        # Slug
        if category["image"] == "":
            head_image = category["family__image"]
        else:
            head_image = category["image"]

        context["head_image"] = head_image
        context["icon_image"] = category["family__icon"]

        context["meta_title"] = category["meta_title"]
        context["meta_description"] = category["meta_description"]
        context["meta_keywords"] = category["meta_keywords"]

        context["category"] = category
        context["title"] = (category["slug"], category["name"])
        context["subcategories"] = self.get_subcategory(
            lang, category=category["pk"], show_all=True
        )
        context["menu"]["subcategories"] = context["subcategories"]
        context["outstanding"] = self.get_outstanding_product(
            lang, category=category["pk"]
        )
        context["recommended"] = self.get_recommended_product(
            lang, category=category["pk"]
        )
        context["products"] = self.get_products(lang, category_pk=category["pk"])
        context["slugs"] = [
            (reverse_lazy("home"), _("Home")),
            (category["slug"], category["name"]),
        ]
        context["select"] = (category["slug_family"], category["slug"])
        return context

    def get(self, request, *args, **kwargs):
        raise Http404()
        raise Exception("Definir condiciones")

    def __get_features_subcategory(self, lang, subcategory_pk):
        return self.__get_features_and_attributes_subcategory(
            lang, subcategory_pk, ProductFeature
        )

    def __get_attributes_subcategory(self, lang, subcategory_pk):
        return self.__get_features_and_attributes_subcategory(
            lang, subcategory_pk, ProductFinalAttribute
        )

    def __get_features_and_attributes_subcategory(
        self, lang, subcategory_pk, MODEL_RELATED
    ):
        if MODEL_RELATED == ProductFeature:
            relation = "product__product_features"
            related = "feature"
            field_list_value = "feature"
            related_by_subcategory = "product__subcategory"
            related_with_product_final = "product__products_final"
            MODEL_OPTION_VALUE = OptionValueFeature
        else:
            # ProductFinalAttribute
            relation = "products_final_attr"
            related = "attribute"
            field_list_value = "attribute"
            related_by_subcategory = "product__product__subcategory"
            related_with_product_final = "product"
            MODEL_OPTION_VALUE = OptionValueAttribute

        items_list = []
        qs = (
            ProductFinal.objects.filter(
                **{
                    "product__subcategory__pk": subcategory_pk,
                    "product__products_image__principal": True,
                    "{}__public".format(lang): True,
                }
            )
            .exclude(
                **{
                    "{}".format(relation): None,
                    "{}__{}__pk".format(relation, related): None,
                }
            )
            .values(
                "{}__{}__pk".format(relation, related),
                "{}__{}__list_value".format(relation, related),
                "{}__{}__type_value".format(relation, related),
                "{}__{}__{}__description".format(relation, related, lang),
            )
            .annotate(
                pk=F("{}__{}__pk".format(relation, related)),
                list_value=F("{}__{}__list_value".format(relation, related)),
                type_value=F("{}__{}__type_value".format(relation, related)),
                description=F(
                    "{}__{}__{}__description".format(relation, related, lang)
                ),
            )
            .order_by("{}__{}__order".format(relation, related))
            .distinct()
        )

        for item in qs:
            if item["type_value"] == TYPE_VALUE_LIST:
                item["values"] = (
                    MODEL_OPTION_VALUE.objects.filter(group__pk=item["list_value"])
                    .values("pk", "{}__description".format(lang))
                    .annotate(val=F("pk"), label=F("{}__description".format(lang)))
                    .order_by("{}__description".format(lang))
                )

            elif item["type_value"] == TYPE_VALUE_BOOLEAN:
                item["values"] = [
                    {"val": 0, "label": _("No")},
                    {"val": 1, "label": _("Yes")},
                ]
            else:
                item["values"] = (
                    MODEL_RELATED.objects.filter(
                        **{
                            "{}__pk".format(field_list_value): item["pk"],
                            "{}__pk".format(related_by_subcategory): subcategory_pk,
                        }
                    )
                    .exclude(
                        **{"{}__pk__isnull".format(related_with_product_final): True}
                    )
                    .values("pk", "value")
                    .annotate(val=F("value"), label=F("value"))
                    .order_by("value")
                    .distinct()
                )

            if item["values"]:
                item.pop("{}__{}__pk".format(relation, related))
                item.pop("{}__{}__list_value".format(relation, related))
                item.pop("{}__{}__type_value".format(relation, related))
                item.pop("{}__{}__{}__description".format(relation, related, lang))
                items_list.append(item)
        return items_list

    def get_qs(self, slug):
        queryset = []
        for langs in settings.LANGUAGES:
            queryset.append(Q(**{"{}__slug".format(langs[0].lower()): slug}))
        return queryset

    # ya no hace falta, se sustituye por un tags para poder pasarle el template
    def get_slider(self, lang, identifier):
        sliders = []
        for sl in Slider.objects.filter(
            identifier=identifier, sliderelements__public=True
        ).values(
            "sliderelements__{}__title".format(lang),
            "sliderelements__{}__button".format(lang),
            "sliderelements__{}__description".format(lang),
            "sliderelements__{}__image".format(lang),
        ):
            sl["title"] = sl["sliderelements__{}__title".format(lang)]
            sl["button"] = sl["sliderelements__{}__button".format(lang)]
            sl["description"] = sl["sliderelements__{}__description".format(lang)]
            sl["image"] = sl["sliderelements__{}__image".format(lang)]
            sliders.append(sl)
        return sliders

    def get_outstanding_product(
        self, lang, family=None, category=None, subcategory=None
    ):
        return ProductFinal.get_outstanding_products(
            lang, family=family, category=category, subcategory=subcategory
        )
        # return ProductFinal.get_outstanding_products(lang, self.apply_surcharge, category, subcategory)

    def get_recommended_product(
        self, lang, family=None, category=None, subcategory=None
    ):
        return ProductFinal.get_recommended_products(
            lang, family=family, category=category, subcategory=subcategory
        )
        # return ProductFinal.get_recommended_products(lang, self.apply_surcharge, category, subcategory)

    def get_products(
        self,
        lang,
        family_pk=None,
        category_pk=None,
        subcategory_pk=None,
        outstanding=None,
    ):
        conditions = {
            "public": True,
            "products_image__public": True,
            "products_image__principal": True,
        }
        if family_pk:
            conditions["family__pk"] = family_pk
        if category_pk:
            conditions["category__pk"] = category_pk
        if subcategory_pk:
            conditions["subcategory__pk"] = subcategory_pk
        if outstanding:
            conditions["products_final__outstanding"] = True
        queryset = (
            Product.objects.filter(**conditions)
            .distinct()
            .annotate(
                name=F("{}__name".format(lang)),
                slug=F("{}__slug".format(lang)),
                image=F("products_image__image"),
                best_sellers=Sum("products_final__line_order_sales__quantity"),
            )
            .order_by("best_sellers")
        )

        products = []
        for product in queryset:
            attributes = []
            for product_final in product.products_final.all():
                if product_final.weight < 1000:
                    peso = product_final.weight
                    unidad = "g"
                else:
                    peso = product_final.weight / 1000
                    unidad = "Kg"
                # tiene decimales
                if abs(peso) - abs(int(peso)) == 0:
                    formato = "{0:.0f} {1}"
                else:
                    formato = "{0:.2f} {1}"
                attributes.append(formato.format(peso, unidad))
                # attributes.append(self.__get_attributes(product_final))
            product.attributes = attributes
            products.append(product)
        return products

    def get_categories(self, lang, family_pk):
        categories = (
            Category.objects.filter(family__pk=family_pk, public=True)
            .annotate(name=F("{}__name".format(lang)), slug=F("{}__slug".format(lang)))
            .order_by("order", "{}__name".format(lang))
        )
        return categories

    def get_flagship(self, lang):
        return FlagshipProduct.get_flagship(lang)
        return FlagshipProduct.get_flagship(lang, self.apply_surcharge)

    def get_subcategory(self, lang, category=None, show_all=False):
        items = {}
        items_order = []
        query = Q(subcategory__outstanding=True)
        if category is not None:
            query &= Q(category=category)
        for item in (
            Product.objects.filter(query)
            .values(
                "subcategory",
                "subcategory__image",
                "category__{}__slug".format(lang),
                "subcategory__{}__slug".format(lang),
                "subcategory__{}__name".format(lang),
                "subcategory__{}__description".format(lang),
            )
            .order_by(
                "subcategory__order",
                "subcategory__{}__name".format(lang),
            )
            .distinct()
        ):
            if item["subcategory"] not in items:
                aux = {
                    "id": "{}_{}".format(
                        item["category__{}__slug".format(lang)],
                        item["subcategory__{}__slug".format(lang)],
                    ),
                    "slug": "{}/{}".format(
                        item["category__{}__slug".format(lang)],
                        item["subcategory__{}__slug".format(lang)],
                    ),
                    "label": item["subcategory__{}__name".format(lang)],
                    "description": item["subcategory__{}__description".format(lang)],
                    "image": item["subcategory__image"],
                }
                items[item["subcategory"]] = aux
                items_order.append(item["subcategory"])
            else:
                aux = items[item["subcategory"]]
                items[item["subcategory"]] = aux

        result = []
        for o in items_order[:9]:
            result.append(items[o])
        return result

    def range_price(self, lang, subcategory, brand=None):
        qs = ProductFinal.objects.filter(
            **{
                "product__subcategory__pk": subcategory["pk"],
                # "{}__public".format(lang): True
            }
        )
        if brand:
            qs.filter(product__brand__pk=brand["pk"])
        datas = qs.aggregate(Max("price"), Min("price"))
        if datas:
            if datas["price__min"] is None:
                datas["price__min"] = 0
            if datas["price__max"] is None:
                datas["price__max"] = 0
            return [int(datas["price__min"]), int(ceil(datas["price__max"]))]
        return [0, 0]


class SearchProduct(GenSlugLevelGet):
    template_name = "frontend/subcategoria.html"

    def get(self, request, *args, **kwargs):
        lang = get_language_database()
        context = self.context_basic(request, lang)
        query = request.GET.get("query", None)
        if query:
            brands, categories, range_price = self.search_products(query, lang)
            context["brands"] = brands
            context["categories"] = categories
            context["range_price"] = range_price
            context["query"] = query
            context["url"] = reverse_lazy(
                "CDNX_products_list_products_base", kwargs={"type": "SEARCH", "pk": 0}
            )
        else:
            context["error_code"] = "SHP 01"
            context["error_message"] = _("Consulta no definida")
            self.template_name = "frontend/error.html"
            return render(request, self.template_name, context)
            # raise Exception("ups!!! no me has pasado la consulta :(")

        return render(request, self.template_name, context)


class OutstandingProduct(GenSlugLevelGet):
    def get(self, request, *args, **kwargs):
        self.template_name = "frontend/{}.html".format("categoria")

        lang = get_language_database()
        context = self.context_basic(request, lang)
        context["products"] = self.get_products(lang, outstanding=True)
        return render(request, self.template_name, context)


class SlugLevelGet(GenSlugLevelGet):
    def get(self, request, *args, **kwargs):
        # print datetime.datetime.now(), 0
        lang = get_language_database()
        # print datetime.datetime.now(), 1
        context = self.context_basic(request, lang)
        # print datetime.datetime.now(), 2
        slug1 = kwargs["slug1"]
        slug2 = kwargs.get("slug2", None)
        slug3 = kwargs.get("slug3", None)
        # print datetime.datetime.now(), 3

        self.html_response = None
        self.template_name = None

        if slug3:
            context = self.get1slug(lang, context, slug3)
            # context = self.get3slug(lang, context, slug1, slug2, slug3)
        elif slug2:
            context = self.get2slug(lang, context, slug1, slug2)
        elif slug1:
            # print datetime.datetime.now(), 4
            context = self.get1slug(lang, context, slug1)
            # print datetime.datetime.now(), 5
        else:
            # 404 ERROR
            raise Http404()
            # raise Exception("ups!!!")

        if self.html_response:
            return HttpResponse(
                Template("{}".format(self.html_response)).render(Context(context))
            )
        elif self.template_name:
            try:
                return render(request, self.template_name, context)
            except TemplateDoesNotExist:
                lang = get_language_database()
                exclude_words = {
                    "es": [
                        "a",
                        "ante",
                        "bajo",
                        "cabe",
                        "con",
                        "contra",
                        "de",
                        "desde",
                        "durante",
                        "en",
                        "entre",
                        "hacia",
                        "hasta",
                        "mediante",
                        "para",
                        "por",
                        "según",
                        "sin",
                        "so",
                        "sobre",
                        "tras",
                        "versus",
                        "vía",
                        "de",
                        "el",
                        "los",
                        "las",
                        "la",
                        "del",
                        "al",
                    ],
                    "en": [
                        "a",
                        "about",
                        "above",
                        "across",
                        "after",
                        "against",
                        "along",
                        "amid",
                        "among",
                        "and",
                        "around",
                        "as",
                        "at",
                        "away",
                        "before",
                        "below",
                        "beneath",
                        "beside",
                        "between",
                        "beyond",
                        "bottom",
                        "by",
                        "close",
                        "down",
                        "during",
                        "for",
                        "from",
                        "in",
                        "inside",
                        "into",
                        "near",
                        "next",
                        "of",
                        "off",
                        "on",
                        "onto",
                        "out",
                        "outside",
                        "over",
                        "past",
                        "round",
                        "since",
                        "the",
                        "through",
                        "throughout",
                        "till",
                        "to",
                        "top",
                        "towards",
                        "under",
                        "underneath",
                        "until",
                        "up",
                        "upon",
                        "within",
                    ],
                }
                query = []
                words = self.template_name.split("/")[1].split(".")[0].split("-")
                if lang in exclude_words:
                    for word in words:
                        if word not in exclude_words[lang]:
                            query.append(word)
                else:
                    query = words

                query = " ".join(query)

                self.template_name = "frontend/subcategoria.html"

                brands, categories, range_price = self.search_products(query, lang)
                context["brands"] = brands
                context["categories"] = categories
                context["range_price"] = range_price
                context["query"] = query
                context["url"] = reverse_lazy(
                    "CDNX_products_list_products_base",
                    kwargs={"type": "SEARCH", "pk": 0},
                )
                return render(request, self.template_name, context)
        else:
            raise Http404()
            # raise Exception("ups_render!!!")

    """
    URL examples:
    /product
    /brand
    /staticpage
    /subcategory
    /category
    """

    def get1slug(self, lang, context, slug1):
        queryset = self.get_qs(slug1)
        family = self.find_family(lang, slug1)
        product = self.find_product(lang, queryset)
        product_final = self.find_product_final(lang, queryset)
        category = self.find_category(lang, slug1)
        subcategory = self.find_subcategory(lang, slug1)
        # brand = self.find_brand(slug1)
        staticpage = self.find_staticpage(lang, slug1)

        if family:
            # OK
            context = self.is_family(lang, context, family)
        elif product:
            context = self.is_product(lang, context, product)
        elif product_final:
            # OK
            context = self.is_product_final(lang, context, product_final)
        # elif brand:
        #     context = self.is_brand(lang, context, brand)
        elif staticpage:
            # OK
            context = self.is_staticpage(lang, context, staticpage)
        elif category:
            # OK
            context = self.is_category(lang, context, category)
        elif subcategory:
            # OK
            context = self.is_subcategory(lang, context, subcategory)
        else:

            self.template_name = "frontend/{}.html".format(slug1)
            # context['slider'] = self.get_slider(lang, 'home')
            context["subcategorymenu"] = self.get_subcategory(lang)
            context["flagship"] = self.get_flagship(lang)
            context["outstanding"] = self.get_outstanding_product(lang)

        return context

    """
    URL examples:
    /category/subcategory
    /subcategory/brand
    """

    def get2slug(self, lang, context, slug1, slug2):
        subcategory = self.find_subcategory(lang, slug2, slug1)
        # subcategory_only = self.find_subcategory(lang, slug1)
        # brand = self.find_brand(slug2)

        if subcategory:
            context = self.is_subcategory(lang, context, subcategory)
            context["range_price"] = self.range_price(lang, subcategory)
            """
            elif brand and subcategory_only:
                context = self.is_subcategory(lang, context, subcategory_only)
                context['brand_default'] = brand
                context['range_price'] = self.range_price(lang, subcategory_only, brand)
            """
        else:
            self.template_name = "frontend/{}.html".format(slug1)
            # context['slider'] = self.get_slider(lang, 'home')
            context["subcategorymenu"] = self.get_subcategory(lang)
            context["flagship"] = self.get_flagship(lang)
            context["outstanding"] = self.get_outstanding_product(lang)

        return context

    """
    pendiente de definir
    """

    def get3slug(self, lang, context, slug1, slug2, slug3):
        raise Http404()
        raise Exception("slug3")


class BackendUser(GenSlugLevelGet):
    template_name = "frontend/backend_user.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["user"] = getattr(request, "user", None)
        lang = get_language_database()
        context["menu"] = get_menu(lang)
        return render(request, self.template_name, context)


class ShoppingCart(View):
    template_name = "frontend/comprar.html"

    def get(self, request, *args, **kwargs):
        context = {}
        lang = get_language_database()
        context["menu"] = get_menu(lang)
        context["slugs"] = [
            (reverse_lazy("home"), _("Home")),
            (reverse_lazy("shopping_cart"), _("Shopping Cart")),
        ]
        return render(request, self.template_name, context)


class Checkout(View):
    template_name = "frontend/checkout.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Checkout, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {}
        lang = get_language_database()
        context["menu"] = get_menu(lang)
        context["lang"] = lang
        context["slugs"] = [
            (reverse_lazy("home"), _("Home")),
            (reverse_lazy("checkout"), _("Checkout")),
        ]

        context["countries"] = get_country()
        # context['provinces'] = get_provinces()

        context["payments"] = []
        for payment_method in settings.PAYMENTS:
            if payment_method != "meta":
                d = settings.PAYMENTS[payment_method]
                d["payment_method"] = payment_method
                context["payments"].append(d)

        context["transports"] = []
        for transport_method in settings.TRANSPORTS:
            if transport_method != "meta":
                d = settings.TRANSPORTS[transport_method]
                d["transport_method"] = transport_method
                context["transports"].append(d)

        if request.user.is_authenticated():
            person = request.user.person
            # customer = person.customer

            billing_addresses = person.addresses.filter(main_invoice=True)
            if billing_addresses.exists():
                context["billing_address"] = (
                    billing_addresses.only(
                        "pk",
                        "address",
                        "zipcode",
                        "city",
                        "province",
                        "region",
                        "country",
                        "town",
                        "phone",
                        "city__id",
                        "province__id",
                        "region__id",
                        "country__id",
                    )
                    .annotate(
                        city_pk=F("city__id"),
                        province_pk=F("province__id"),
                        region_pk=F("region__id"),
                        country_pk=F("country__id"),
                        city_name=F("city__{}__name".format(lang)),
                        province_name=F("province__{}__name".format(lang)),
                        region_name=F("region__{}__name".format(lang)),
                        country_name=F("country__{}__name".format(lang)),
                    )
                    .first()
                    .__dict__
                )

            context["shipping_addresses"] = (
                person.addresses.filter(main_invoice=False)
                .values(
                    "pk",
                    "address",
                    "zipcode",
                    "city",
                    "province",
                    "region",
                    "country",
                    "town",
                    "phone",
                    "city__id",
                    "province__id",
                    "region__id",
                    "country__id",
                )
                .annotate(
                    city_pk=F("city__id"),
                    province_pk=F("city__province__id"),
                    region_pk=F("city__region__id"),
                    country_pk=F("city__country__id"),
                    city_name=F("city__{}__name".format(lang)),
                    province_name=F("province__{}__name".format(lang)),
                    region_name=F("region__{}__name".format(lang)),
                    country_name=F("country__{}__name".format(lang)),
                )
            )

        cart = ShoppingCartProxy(request)
        context["cart"] = cart
        context.update(cart.get_info_prices(onlypublic=True))

        context["weight"] = 0
        for product in cart.get_products(onlypublic=True)["products"]:
            context["weight"] += product["weight"] * product["quantity"]
        # raise Exception(context['price_total'])

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        answer = {
            "error": None,
            "error_code": None,
        }

        try:
            POST = json.loads(request.body.decode("utf-8"))
        except Exception:
            POST = None

        # customer = None
        billing_address = None
        shipping_address = None
        # shopping_cart = None

        if POST is not None and type(POST) == dict:
            if "billing" in POST and type(POST) == dict:
                billing = POST["billing"]
                generated_password = False

                country_billing = Country.objects.filter(
                    pk=billing.get("country", None)
                ).first()
                if country_billing is None:
                    answer["error"] = _("Country of billing is required")
                    answer["error_code"] = "E05"
                else:
                    region_billing = Region.objects.filter(
                        pk=billing.get("region", None)
                    ).first()
                    # province_billing = Province.objects.filter(pk=billing.get('province', None)).first()
                    province_billing = Province.objects.filter(
                        code=billing.get("province", None)
                    ).first()
                    city_billing = City.objects.filter(
                        pk=billing.get("city", None)
                    ).first()

                    if "shipping" in POST:
                        shipping = POST["shipping"]
                        country_shipping = Country.objects.filter(
                            pk=shipping.get("country", None)
                        ).first()
                        if country_shipping is None:
                            answer["error"] = _("Country of shipping is required")
                            answer["error_code"] = "E05"
                        else:
                            region_shipping = Region.objects.filter(
                                pk=shipping.get("region", None)
                            ).first()
                            # province_shipping = Province.objects.filter(pk=shipping.get('province', None)).first()
                            province_shipping = Province.objects.filter(
                                code=shipping.get("province", None)
                            ).first()
                            city_shipping = City.objects.filter(
                                pk=shipping.get("city", None)
                            ).first()

                if answer["error"] is None:
                    if request.user.is_authenticated():
                        person = request.user.person
                        # customer = person.customer

                        try:
                            billing_address = PersonAddress.objects.get(
                                person=person, main_invoice=True
                            )
                            billing_address.city = City.objects.filter(
                                pk=billing.get("city", None)
                            ).first()
                            billing_address.zipcode = billing.get("zipcode", None)
                            billing_address.address = billing.get("address", None)
                            billing_address.phone = billing.get("phone", None)
                        except ObjectDoesNotExist:
                            billing_address = PersonAddress(
                                person=person,
                                country=country_billing,
                                region=region_billing,
                                province=province_billing,
                                city=city_billing,
                                zipcode=billing.get("zipcode", None),
                                address=billing.get("address", None),
                                phone=billing.get("phone", None),
                                town=billing.get("town", None),
                                main_invoice=True,
                            )
                        billing_address.save()

                        if "shipping_pk" in POST:
                            shipping_address = PersonAddress.objects.get(
                                pk=int(POST["shipping_pk"])
                            )
                        elif "shipping" in POST:
                            shipping = POST["shipping"]
                            shipping_address = PersonAddress(
                                person=person,
                                country=country_shipping,
                                region=region_shipping,
                                province=province_shipping,
                                city=city_shipping,
                                zipcode=shipping.get("zipcode", None),
                                address=shipping.get("address", None),
                                phone=shipping.get("phone", None),
                                town=shipping.get("town", None),
                                main_delivery=True,
                            )
                            shipping_address.save()
                        else:
                            shipping_address = billing_address
                    else:

                        password = POST.get("password", None)
                        if password is None:
                            password = uuid.uuid4().hex
                            generated_password = True

                        lang = get_language_database()
                        try:
                            user, password = create_user(
                                first_name=billing.get("first_name", None),
                                last_name=billing.get("last_name", None),
                                email=billing.get("email", None),
                                password=password,
                                lang=lang,
                            )

                        except ValueError:
                            answer["error"] = _("Email address already registered")
                            answer["error_code"] = "E02"
                            user = None

                        if user:
                            billing_address = PersonAddress(
                                person=user.person,
                                country=country_billing,
                                region=region_billing,
                                province=province_billing,
                                city=city_billing,
                                zipcode=billing.get("zipcode", None),
                                address=billing.get("address", None),
                                phone=billing.get("phone", None),
                                town=billing.get("town", None),
                                main_invoice=True,
                            )
                            billing_address.save()

                            if "shipping" in POST:
                                if type(POST["shipping"]) == dict:
                                    shipping = POST["shipping"]
                                    shipping_address = PersonAddress(
                                        person=user.person,
                                        country=country_shipping,
                                        region=region_shipping,
                                        province=province_shipping,
                                        city=city_shipping,
                                        zipcode=shipping.get("zipcode", None),
                                        address=shipping.get("address", None),
                                        phone=shipping.get("phone", None),
                                        town=shipping.get("town", None),
                                        main_delivery=True,
                                    )
                                    shipping_address.save()
                                else:
                                    answer["error"] = _(
                                        "shipping POST parameter must be a dictionary"
                                    )
                                    answer["error_code"] = "E04"

                            else:
                                shipping_address = billing_address

                            user = authenticate(
                                username=POST["billing"]["email"], password=password
                            )
                            login(request, user)

                if answer["error"] is None:
                    shopping_proxy = ShoppingCartProxy(request)
                    # shopping_cart = shopping_proxy.user_cart
                    shopping_proxy.set_address(billing_address, shipping_address)
                    # Remove old transport
                    lines = shopping_proxy.list()
                    for line in lines:
                        p = line.product
                        if p.product.code == "MRW":
                            shopping_proxy.remove(p.pk)
                            p.delete()
                    # If transport
                    zipcode = POST.get("shipping", POST.get("billing", {})).get(
                        "zipcode", None
                    )
                    country = POST.get("shipping", POST.get("billing", {})).get(
                        "country", None
                    )
                    if POST.get("transport", None) and zipcode and country:
                        # Calculate total weight
                        total_weight = 0.0
                        lines = shopping_proxy.list()
                        for line in lines:
                            if line.product.weight is not None:
                                total_weight += line.product.weight * line.quantity
                            else:
                                total_weight += (
                                    line.product.product.weight * line.quantity
                                )
                        # Prepare query for transport
                        query = {
                            "country": str(country),
                            "zipcode": str(zipcode),
                            "weight": str(total_weight),
                        }
                        # Transport price
                        prices = TransportCalculate.calculator(query)
                        if not prices.get("error", None):
                            price = (
                                prices.get("rates", {})
                                .get("mrw", {})
                                .get("price", None)
                            )
                            if price is not None and price >= 0.0:
                                # Set new transport
                                pf = ProductFinal()
                                pf.product = Product.objects.get(code="MRW")
                                pf.price = price
                                pf.price_base = price
                                pf.price_base_local = price
                                pf.save()
                                for lang_code in settings.LANGUAGES_DATABASES:
                                    clss = "ProductFinalText{}".format(lang_code)
                                    i = eval(clss)()
                                    i.name = _("Transporte")
                                    i.product = pf
                                    i.slug = "tempslug{}".format(pf.pk)
                                    i.public = False
                                    i.save()
                                # Add new transport to shopping cart
                                shopping_proxy.add(pf.pk, 1)
                            else:
                                answer["error"] = _("Tranport rate not found")
                                answer["error_code"] = "E07"
                        else:
                            answer["error"] = "{}: {}".format(
                                _("Transport rate error"), prices["error"]
                            )
                            answer["error_code"] = "E06"

                    if generated_password:
                        pass  # TODO: Send email with password

                    # raise Exception('TODO: Prepare the shipping here')
                    if not prices.get("error", None):
                        answer["url"] = reverse_lazy(
                            "checkout_pay", kwargs={"payment_method": POST["payment"]}
                        )
            else:
                answer["error"] = _("Missing billing address from request dictionary")
                answer["error_code"] = "E03"
        else:
            answer["error"] = _("Could not decode the json from POST")
            answer["error_code"] = "E01"

        return JsonResponse(answer)


class CheckoutPayment(View):
    template_name = "frontend/checkout-temporal.html"

    def get(self, request, *args, **kwargs):
        context = {}
        lang = get_language_database()
        context["menu"] = get_menu(lang)
        context["slugs"] = [
            (reverse_lazy("home"), _("Home")),
            (reverse_lazy("checkout"), _("Checkout")),
        ]
        context["version"] = settings.VERSION

        emails_admin = []
        for (name, email) in settings.ADMINS:
            emails_admin.append(email)

        cart = ShoppingCartProxy(request)
        shopping_cart = cart.user_cart
        info_prices = cart.get_info_prices()
        # shopping_cart.pass_to_budget()

        pm = kwargs.get("payment_method", None)

        if shopping_cart:
            if hasattr(settings, "PAYMENTS") and pm in settings.PAYMENTS:
                pm = list(settings.PAYMENTS.keys())
                pm.remove("meta")
                pay_method = PaymentMethod()
                context["order"] = shopping_cart.pk
                info = pay_method.pay(
                    pm[0], "confirm_payment", info_prices["price_total"], shopping_cart
                )
                if info["error"]:
                    context["error_code"] = info["error_code"]
                    context["error_message"] = info["error_message"]
                else:
                    context["btn"] = info["btn"]
            else:
                context["error_code"] = "CP 001"
                context["error_message"] = _("Metodo de pago desconocido")
        else:
            context["error_code"] = "CP 002"
            context["error_message"] = _("No hay carrito de la compra")

        if "error_code" in context:
            if settings.DEBUG:
                legacy = False
            else:
                legacy = True
            for email in emails_admin:
                email_message = EmailMessage()
                email_message.efrom = settings.DEFAULT_FROM_EMAIL
                email_message.eto = email
                email_message.subject = "[{}] {}".format(
                    settings.INFO_PROJECT["name_project"], _("Checkout Payment Error")
                )
                email_message.body = "Hello:\n\nThere was an exception while using CheckoutPayment, code: {error_code}, there is some problem :\n\n{error_message}\n\nThank you,\n\n--{name_project} Helper v({version})".format(
                    error_code=context["error_code"],
                    error_message=context["error_message"],
                    version=context["version"],
                    name_project=settings.INFO_PROJECT["name_project"],
                )
                email_message.save()
                email_message.send(legacy=legacy, silent=True)

            self.template_name = "frontend/error.html"
            return render(request, self.template_name, context)
        else:
            shopping_cart.expiration_date = timezone.now()
            shopping_cart.save()
            return render(request, self.template_name, context)


class ConfirmPayment(View):
    template_name = "frontend/checkout-completo.html"

    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        context = {}
        lang = get_language_database()
        context["menu"] = get_menu(lang)

        locator = kwargs.get("locator", None)
        action = kwargs.get("action", None)
        error = kwargs.get("error", None)

        # Si en error viene un valor distinto a 0 significa que hay un error
        if error != "0":
            # Hace falta extraer los textos a partir del error.
            context["error"] = True
            context["error_message"] = _("Hay un error de tipo: {}".format(error))
        else:
            if action == "confirm":
                context["action"] = _("Pago realizado correctamente")
            elif action == "cancel":
                context["action"] = _("Pago cancelado")
                self.template_name = "frontend/checkout-cancelado.html"
            else:
                context["error"] = True
                context["error_message"] = "Accion desconocida({})".format(action)

        # Extract order selected
        if locator is None:
            context["error"] = True
            context["error_message"] = "Accion desconocida({})".format(action)
        else:
            paymentrequest = PaymentRequest.objects.filter(locator=locator).first()
            if paymentrequest:
                budget = SalesBasket.objects.filter(payment=paymentrequest).first()
                if budget:
                    budget.expiration_date = None
                    budget.save()
                context["budget"] = budget

        return render(self.request, self.template_name, context)

    @staticmethod
    def payment_paid(request, locator):
        paymentrequest = PaymentRequest.objects.get(locator=locator)  # .first()
        lang = get_language()
        if paymentrequest:
            # busca el presupuesto del pago
            budget = SalesBasket.objects.get(payment=paymentrequest)  # .first()

            if budget:
                # creo pedido
                # relaciono pedido con budget
                with transaction.atomic():
                    # pasamos el presupuesto a pedido
                    ctx = budget.pass_to_order(paymentrequest)
                    if ctx["error"]:
                        raise Exception(ctx["error"])
                    else:
                        context = {"budget": budget}

                        email_customer = budget.customer.external.CDNX_get_email()

                        # enviar email/notificacion al cliente
                        send_email("NUEVACOMPRA01", lang, context, email_customer)
                        context["email_customer"] = email_customer
                        # enviar email/notificacion a la tienda
                        for email in settings.CLIENTS:
                            send_email("NUEVACOMPRAADMIN01", lang, context, email[1])
            else:
                # no existe el presupuesto
                # enviar email/notificacion a la tienda
                context = {
                    "locator": locator,
                    "paymentrequest": paymentrequest,
                }
                for email in settings.CLIENTS:
                    send_email("BUDGETNOTFOUNDADMIN01", lang, context, email[1])
        else:
            # enviar email/notificacion de para los administradores
            subject = (_("Payment request does not exist"),)
            body = _(
                """
Hello:

There was an exception while using payment_paid() function in class ConfirmPayment, the paymentrequest doesn't exist. Locator is: {locator}

Thank you"""
            ).format({"locator": locator})
            send_email_admins(subject, body)

    @staticmethod
    def payment_exception(request, pk, e):
        budget = SalesBasket.objects.filter(pk=pk).first()
        if budget:
            budget_code = budget.code
        else:
            budget_code = _("Unknown code (pk=%(pk))") % {"pk": pk}

        msg = "Hello \n\n"
        msg += "There was an exception in payments of the budget {budget}, there is some problem:\n\n"
        msg += "\n\n{e}\n\n\n\n"
        msg += "Thank you,\n\n"

        subject = (_("Payment Exception"),)
        body = _(msg).format(e=e, budget=budget_code)
        send_email_admins(subject, body)


class ListProductsFrontend(GenList):
    public = True
    model = Product
    gentrans = {
        "buy": _("Buy"),
        "new": _("New"),
        "wishlist": _("Wish list"),
        "shoppingcart": _("Shopping cart"),
    }

    def __fields__(self, info):
        lang = get_language_database()
        fields = []
        fields.append(("name:{}__name".format(lang), _("Name")))
        fields.append(("slug:{}__slug".format(lang), _("Slug")))
        fields.append(("products_image__image", _("Image")))
        fields.append(("products_image__principal", _("Principal")))
        # fields.append(('productfinals_image__image', _("Image")))
        # fields.append(('productfinals_image__principal', _("Principal")))
        # fields.append(('price', _("Price")))
        # fields.append(('price_old:price', _("Price")))
        # fields.append(('offer', _("Offer")))
        fields.append(("created", _("Created")))
        # fields.append(('reviews_value', _("reviews_value")))
        # fields.append(('reviews_count', _("reviews_count")))
        return fields

    def __limitQ__(self, info):
        limits = {}
        pk = self.kwargs.get("pk", None)
        type_list = self.kwargs.get("type", None)
        # get language
        lang = get_language_database()

        if pk and type_list:
            # aplicamos los filtros recibidos
            params = ast.literal_eval(info.request.GET.get("json"))

            slug_subcategory = None
            if "subcategory" in params and params["subcategory"]:
                if params["subcategory"] != "*":
                    slug_subcategory = params["subcategory"]

            slug_type = None
            if "brand" in params and params["brand"]:
                if params["brand"] != "*":
                    slug_type = params["brand"]

            slug_family = None
            if "family" in params and params["family"]:
                if params["family"] != "*":
                    slug_family = params["family"]

            only_with_stock = None
            # filtramos dependiendo de la url original que estemos visitando
            if type_list == "SUB":
                only_with_stock = Category.objects.filter(
                    subcategory__pk=pk, show_only_product_stock=True
                ).exists()
                limits["type_list"] = Q(subcategory__pk=pk)

            elif type_list == "CAT":
                limits["type_list"] = Q(category__pk=pk)

            elif type_list == "BRAND":
                limits["type_list"] = Q(brand__pk=pk)

            elif type_list == "SEARCH":
                only_with_stock = settings.CDNX_PRODUCTS_SHOW_ONLY_STOCK

            else:
                raise Exception("Pendiente de definir")

            if slug_subcategory:
                limits["by_sucategory"] = Q(
                    **{"subcategory__{}__slug".format(lang): slug_subcategory}
                )

            if slug_type:
                limits["by_brand"] = Q(**{"brand__{}__slug".format(lang): slug_type})

            if slug_family:
                limits["by_family"] = Q(**{"family__{}__slug".format(lang): slug_type})

            # aplicamos los filtros recibidos
            params = ast.literal_eval(info.request.GET.get("json"))
            if "filters" in params and params["filters"]:
                filters = params["filters"]
                if "brand" in filters and filters["brand"]:
                    limits["product__brand"] = Q(brand__in=filters["brand"])
                if "feature" in filters and filters["feature"]:
                    for feature in filters["feature"]:
                        if feature and filters["feature"][feature]:
                            limits["product_features__feature"] = Q(
                                product_features__feature__pk=feature,
                                product_features__value__in=filters["feature"][feature],
                            )

                if "subcategory" in filters and filters["subcategory"]:
                    for subcategory in filters["subcategory"]:
                        limits["product__subcategory"] = Q(
                            subcategory__pk__in=[int(x) for x in filters["subcategory"]]
                        )

                if "query" in filters and filters["query"]:
                    filters_txt = [
                        "{}__name__icontains".format(lang),
                        "{}__slug__icontains".format(lang),
                        "code__icontains",
                        # "product__code__icontains",
                        # "product__model__icontains",
                        # "product__{}__name__icontains".format(lang),
                        # "product__{}__slug__icontains".format(lang),
                        "brand__{}__name__icontains".format(lang),
                        "brand__{}__slug__icontains".format(lang),
                        "category__{}__name__icontains".format(lang),
                        "category__{}__slug__icontains".format(lang),
                        "subcategory__{}__name__icontains".format(lang),
                        "subcategory__{}__slug__icontains".format(lang),
                    ]
                    queryset_custom = None
                    for filter_txt in filters_txt:
                        queryset_custom_and = None
                        for word in filters["query"].split():
                            if queryset_custom_and:
                                queryset_custom_and &= Q(**{filter_txt: word})
                            else:
                                queryset_custom_and = Q(**{filter_txt: word})
                        if queryset_custom:
                            queryset_custom |= queryset_custom_and
                        else:
                            queryset_custom = queryset_custom_and

                    limits["query"] = queryset_custom

                if ("force_image" not in filters) or (
                    "force_image" in filters and filters["force_image"] == 1
                ):
                    limits["image"] = Q(products_image__principal=True)

            if only_with_stock is None:
                only_with_stock = settings.CDNX_PRODUCTS_SHOW_ONLY_STOCK

            """
            if only_with_stock and hasattr(self.model, 'product_stocks'):
                limits['force_stock'] = reduce(operator.or_, (
                    Q(product__force_stock=True, product_stocks__quantity__gt=0),
                    Q(product__force_stock=False)
                ))
            """

        return limits

    def json_builder(self, answer, context):
        body = self.bodybuilder(context["object_list"], self.autorules())
        products = []
        for product in body:
            temp = product.copy()
            # image principal
            pos_image_ppal = [
                i
                for i, x in enumerate(product["products_image__principal"])
                if x == "True"
            ]

            if len(pos_image_ppal) == 0:
                image = None
            else:
                image = temp["products_image__image"][pos_image_ppal[0]]
            temp["image"] = image
            # is new?
            created = None
            for date_format in getattr(settings, "DATETIME_INPUT_FORMATS", []):
                try:
                    created = datetime.datetime.strptime(temp["created"], date_format)
                    break
                except ValueError:
                    pass
            if (
                created
                and (abs(int(time.time() - time.mktime(created.timetuple()))))
                / (3600 * 24)
                <= settings.CDNX_PRODUCTS_NOVELTY_DAYS
            ):
                temp["new"] = 1
            else:
                temp["new"] = 0

            attrs = {}
            for pfa in ProductFinalAttribute.objects.filter(
                product__product__pk=product["pk"]
            ).order_by("attribute__order"):
                if pfa.product not in attrs:
                    attrs[pfa.product.pk] = []

                if pfa.attribute.type_value == TYPE_VALUE_BOOLEAN:
                    value = bool(pfa.value) and _("True") or _("False")
                elif pfa.attribute.type_value == TYPE_VALUE_FREE:
                    value = pfa.value
                elif pfa.attribute.type_value == TYPE_VALUE_LIST:
                    lang = get_language_database()
                    field = "{}__description".format(lang)
                    ov = (
                        OptionValueAttribute.objects.filter(
                            group=pfa.attribute.list_value, pk=int(pfa.value)
                        )
                        .values(field)
                        .first()
                    )
                    if ov:
                        value = ov[field]
                    else:
                        value = None
                if value:
                    attrs[pfa.product.pk].append(value)

            temp["attrs"] = attrs
            # clean info
            temp.pop("products_image__image")
            temp.pop("products_image__principal")
            temp.pop("created")

            products.append(temp)

        answer["table"]["body"] = products
        return answer


class Sitemap(View):
    template_name = "frontend/sitemap.html"

    def get(self, request, *args, **kwargs):
        context = {}
        lang = get_language_database()
        context["menu"] = get_menu(lang)
        context["slugs"] = [
            (reverse_lazy("home"), _("Home")),
            (reverse_lazy("checkout"), _("Checkout")),
        ]
        context["version"] = settings.VERSION
        info = {}
        for family in Family.objects.filter(public=True).order_by("order"):
            text = getattr(family, lang)
            info[family.pk] = {
                "label": text.name,
                "slug": text.slug,
                "categories": {},
                "products": {},
            }
            for category in family.categories.filter(public=True).order_by("order"):
                text = getattr(category, lang)
                info[family.pk]["categories"][category.pk] = {
                    "label": text.name,
                    "slug": text.slug,
                    "subcategories": {},
                    "products": {},
                }
                for subcategory in category.subcategory.filter(public=True).order_by(
                    "order"
                ):
                    text = getattr(subcategory, lang)
                    info[family.pk]["categories"][category.pk]["subcategories"][
                        subcategory.pk
                    ] = {
                        "label": text.name,
                        "slug": text.slug,
                        "products": {},
                    }
        context["datas"] = info

        return render(request, self.template_name, context)
