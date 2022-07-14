# -*- coding: utf-8 -*-
from django.conf import settings
from codenerix_geodata.models import MODELS as MODELS_GEODATA
from codenerix_invoicing.models import MODELS as MODELS_INVOICING
from codenerix_products.models import MODELS_SLIDERS, MODELS_BRANDS, MODELS_PRODUCTS, MODELS, MODELS_SLUG, MODELS_PRODUCTS_FINAL
from codenerix_cms.models import MODELS as MODELS_CMS


# Helper functions
def lperm(name):
    return ['list_%s' % (name)]


def detperm(name):
    return ['detail_%s' % (name)]


def aperm(name):
    return ['add_%s' % (name)]


def eperm(name):
    return ['change_%s' % (name)]


def delperm(name):
    return ['delete_%s' % (name)]


def wperm(name):
    return ['add_%s' % (name), 'change_%s' % (name), 'delete_%s' % (name), ]


def roperm(name):
    return ['list_%s' % (name), 'detail_%s' % (name), ]


def rwperm(name):
    return ['list_%s' % (name), 'detail_%s' % (name), 'add_%s' % (name), 'change_%s' % (name), ]


def allperm(name):
    return ['list_%s' % (name), 'view_%s' % (name), 'detail_%s' % (name), 'add_%s' % (name), 'change_%s' % (name), 'delete_%s' % (name), ]


geo_name = []
for field, model in MODELS_GEODATA:
    for lang_code in settings.LANGUAGES_DATABASES:
        geo_name += allperm('{}GeoName{}'.format(model, lang_code))

type_document = []
for info in MODELS_INVOICING:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        type_document += allperm("{}Text{}".format(model, lang_code))

cms = []
for info in MODELS_CMS:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        type_document += allperm("{}Text{}".format(model, lang_code))

products = []
for info in MODELS:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        products += allperm("{}Text{}".format(model, lang_code))

for info in MODELS_SLUG:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        products += allperm("{}Text{}".format(model, lang_code))

for info in MODELS_BRANDS + MODELS_PRODUCTS + MODELS_PRODUCTS_FINAL:
    field = info[0]
    model_source = info[1]
    model_relate = info[2]
    for lang_code in settings.LANGUAGES_DATABASES:
        products += allperm("{}Text{}".format(model_source, lang_code))


for info in MODELS_SLIDERS:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        products += allperm("class {}Text{}".format(model, lang_code))


CDNX_PERMISSIONS = {
    'publicist':
        [] +
        # news
        allperm('News') +
        # codenerix_corporate
        allperm('CorporateImage') +
        # codenerix_products
        allperm('TypeTax') +
        allperm('Family') +
        allperm('Category') +
        allperm('Subcategory') +
        allperm('GroupValueFeature') +
        allperm('GroupValueAttribute') +
        allperm('GroupValueFeatureSpecial') +
        allperm('OptionValueFeature') +
        allperm('OptionValueAttribute') +
        allperm('OptionValueFeatureSpecial') +
        allperm('Feature') +
        allperm('Attribute') +
        allperm('FeatureSpecial') +
        allperm('Brand') +
        allperm('Product') +
        allperm('ProductRelationSold') +
        allperm('ProductImage') +
        allperm('ProductDocument') +
        allperm('ProductFinal') +
        allperm('ProductFinalImage') +
        allperm('ProductFinalAttribute') +
        allperm('ProductFeature') +
        allperm('ProductUnique') +
        allperm('FlagshipProduct') +
        allperm('ProductFinalOption') +
        products +
        # codenerix_cms
        allperm('Slider') +
        allperm('SliderElement') +
        allperm('Staticheader') +
        allperm('StaticheaderElement') +
        allperm('StaticPage') +
        cms +
        # codenerix_emails
        allperm('EmailTemplate') +
        # common
        allperm('PublicContact'),

    'XX_other_XX':
        [] +
        # people
        allperm('Person') +
        allperm('PersonAddress') +
        allperm('PersonDependent') +
        allperm('Company') +
        # news
        allperm('News') +
        # codenerix_email
        allperm('EmailMessage') +
        allperm('EmailAttachment') +
        allperm('EmailTemplate') +
        # codenerix_geodata
        allperm('Continent') +
        allperm('Country') +
        allperm('TimeZone') +
        allperm('Region') +
        allperm('Province') +
        allperm('City') +
        geo_name +
        # codenerix_invoicing
        allperm('BillingSeries') +
        allperm('LegalNote') +
        allperm('TypeDocument') +
        allperm('TypeDocumentText') +
        type_document +
        allperm('ProductStock') +
        allperm('StockMovement') +
        allperm('StockMovementProduct') +
        allperm('Haulier') +
        # codenerix_invoicing_sales
        allperm('Customer') +
        allperm('Address') +
        allperm('CustomerDocument') +
        allperm('SalesReservedProduct') +
        allperm('SalesBasket') +
        allperm('SalesLineBasket') +
        allperm('SalesLineBasketOption') +
        allperm('SalesOrder') +
        allperm('SalesLineOrder') +
        allperm('SalesLineOrderOption') +
        allperm('SalesAlbaran') +
        allperm('SalesLineAlbaran') +
        allperm('SalesTicket') +
        allperm('SalesLineTicket') +
        allperm('SalesTicketRectification') +
        allperm('SalesLineTicketRectification') +
        allperm('SalesInvoice') +
        allperm('SalesLineInvoice') +
        allperm('SalesInvoiceRectification') +
        allperm('SalesLineInvoiceRectification') +
        allperm('ReasonModification') +
        allperm('ReasonModificationLineBasket') +
        allperm('ReasonModificationLineOrder') +
        allperm('ReasonModificationLineAlbaran') +
        allperm('ReasonModificationLineTicket') +
        allperm('ReasonModificationLineTicketRectification') +
        allperm('ReasonModificationLineInvoice') +
        allperm('ReasonModificationLineInvoiceRectification') +
        allperm('PrintCounterDocumentBasket') +
        allperm('PrintCounterDocumentOrder') +
        allperm('PrintCounterDocumentAlbaran') +
        allperm('PrintCounterDocumentTicket') +
        allperm('PrintCounterDocumentTicketRectification') +
        allperm('PrintCounterDocumentInvoice') +
        allperm('PrintCounterDocumentInvoiceRectification') +
        # codenerix_invoicing_purchases
        allperm('Provider') +
        allperm('PurchasesBudget') +
        allperm('PurchasesLineBudget') +
        allperm('PurchasesBudgetDocument') +
        allperm('PurchasesOrder') +
        allperm('PurchasesLineOrder') +
        allperm('PurchasesOrderDocument') +
        allperm('PurchasesAlbaran') +
        allperm('PurchasesLineAlbaran') +
        allperm('PurchasesAlbaranDocument') +
        allperm('PurchasesTicket') +
        allperm('PurchasesLineTicket') +
        allperm('PurchasesTicketDocument') +
        allperm('PurchasesTicketRectification') +
        allperm('PurchasesLineTicketRectification') +
        allperm('PurchasesTicketRectificationDocument') +
        allperm('PurchasesInvoice') +
        allperm('PurchasesLineInvoice') +
        allperm('PurchasesInvoiceDocument') +
        allperm('PurchasesInvoiceRectification') +
        allperm('PurchasesLineInvoiceRectification') +
        allperm('PurchasesInvoiceRectificationDocument') +
        # codenerix_corporate
        allperm('CorporateImage') +
        # codenerix_products
        allperm('TypeTax') +
        allperm('Family') +
        allperm('Category') +
        allperm('Subcategory') +
        allperm('GroupValueFeature') +
        allperm('GroupValueAttribute') +
        allperm('GroupValueFeatureSpecial') +
        allperm('OptionValueFeature') +
        allperm('OptionValueAttribute') +
        allperm('OptionValueFeatureSpecial') +
        allperm('Feature') +
        allperm('Attribute') +
        allperm('FeatureSpecial') +
        allperm('Brand') +
        allperm('Product') +
        allperm('ProductRelationSold') +
        allperm('ProductImage') +
        allperm('ProductDocument') +
        allperm('ProductFinal') +
        allperm('ProductFinalImage') +
        allperm('ProductFinalAttribute') +
        allperm('ProductFeature') +
        allperm('ProductUnique') +
        allperm('FlagshipProduct') +
        allperm('ProductFinalOption') +
        products +
        # codenerix_payments
        allperm('Currency') +
        allperm('PaymentRequest') +
        allperm('PaymentConfirmation') +
        allperm('PaymentAnswer') +
        # codenerix_storages
        allperm('GenStorage') +
        allperm('GenStorageContact') +
        allperm('Storage') +
        allperm('StorageContact') +
        allperm('StorageZone') +
        allperm('StorageBatch') +
        # transports
        allperm('TransportZone') +
        allperm('TransportRate') +
        # codenerix_reviews
        allperm('Reviews') +
        # codenerix_emails
        allperm('EmailTemplate') +
        # common
        allperm('PublicContact')
}
"""
        # accounting
        allperm('CashDiary') +

        # codenerix_pos
        allperm('POSPlant') +
        allperm('POSZone') +
        allperm('POSHardware') +
        allperm('POS') +
        allperm('POSSlot') +
        allperm('POSProduct') +
        allperm('POSLog') +
        allperm('POSOperator') +

        # people
        allperm('Publicist') +

        # codenerix_invoicing_cash
        allperm('CashDiary') +
        allperm('CashMovement') +
"""
