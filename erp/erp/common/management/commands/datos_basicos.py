from django.core.management.base import BaseCommand
from django.conf import settings

from codenerix_lib.debugger import Debugger
from codenerix_products.models import TypeTax, Family, Category, Subcategory, MODELS_SLUG, MODELS_BRANDS, MODELS_PRODUCTS, Product, ProductFinal

from codenerix_invoicing.models import BillingSeries
from codenerix_invoicing.models_sales import Customer
from codenerix_pos.models import *

from erp.people.models import Person

for info in MODELS_SLUG + MODELS_BRANDS + MODELS_PRODUCTS:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "from codenerix_products.models import {}Text{}\n".format(model, lang_code)
        print(query)
        exec(query)


class Command(BaseCommand, Debugger):

    def handle(self, *args, **options):
        print("Creando Family")
        code = 'f1'
        family = Family.objects.filter(code=code).first()
        if not family:
            family = Family()
            family.code = code
            family.save()

            for lang_code in settings.LANGUAGES_DATABASES:
                model = eval("FamilyText{}".format(lang_code))
                obj = model()
                obj.family = family
                obj.slug = 'f1'
                obj.name = 'f1'
                obj.description = 'f1'
                obj.save()

        print("Creando Category")
        code = 'c'
        category = Category.objects.filter(code=code).first()
        if not category:
            category = Category()
            category.family = family
            category.code = code
            category.save()

            for lang_code in settings.LANGUAGES_DATABASES:
                model = eval("CategoryText{}".format(lang_code))
                obj = model()
                obj.category = category
                obj.slug = code
                obj.name = code
                obj.description = code
                obj.save()

        print("Creando Subcategory")
        for code in ['sc', ] + ["sc{}".format(x) for x in range(0, 20)]:
            subcategory = Subcategory.objects.filter(code=code).first()
            if not subcategory:
                subcategory = Subcategory()
                subcategory.category = category
                subcategory.code = code
                subcategory.save()

                for lang_code in settings.LANGUAGES_DATABASES:
                    model = eval("SubcategoryText{}".format(lang_code))
                    obj = model()
                    obj.subcategory = subcategory
                    obj.slug = code
                    obj.name = code
                    obj.description = code
                    obj.save()

        print("Creando BillingSeries")
        code = 'A'
        bs = BillingSeries.objects.filter(code=code).first()
        if not bs:
            bs = BillingSeries()
            bs.code = code
            bs.save()

        print("Creando TypeTax")
        code = '21'
        tax = TypeTax.objects.filter(name=code).first()
        if not tax:
            tax = TypeTax()
            tax.name = code
            tax.tax = int(code)
            tax.recargo_equivalencia = 0
            tax.save()

        print "Creando Product"
        codes = ['q1', 'q2'] + ["product{}".format(x) for x in range(0, 20)]
        # ProductFinal.objects.filter(product__code__in=codes).delete()
        # Product.objects.filter(code__in=codes).delete()

        products = []
        for code in codes:
            product = Product.objects.filter(code=code).first()
            if not product:
                product = Product()
                product.code = code
                product.family = family
                product.category = category
                product.subcategory = subcategory
                product.tax = tax
                product.price_base = 12
                product.save()

                for lang_code in settings.LANGUAGES_DATABASES:
                    model = eval("ProductTextText{}".format(lang_code))
                    obj = model()
                    obj.product = product
                    obj.slug = code
                    obj.name = code
                    obj.public = True
                    obj.save()

            print("Creando ProductFinal: {}".format(code))
            pf = ProductFinal.objects.filter(product=product).first()
            if not pf:
                pf = ProductFinal()
                pf.product = product
                pf.save()

                for lang_code in settings.LANGUAGES_DATABASES:
                    model = eval("ProductFinalText{}".format(lang_code))
                    obj = model()
                    obj.product = pf
                    obj.slug = code
                    obj.name = code
                    obj.public = True
                    obj.save()
            products.append(pf)

        print("Creando CorporateImage")
        corporate_image = CorporateImage.objects.first()
        if not corporate_image:
            corporate_image = CorporateImage()
            corporate_image.save()

        print("Creando POSPlant")
        code = 'plant'
        plant = POSPlant.objects.filter(name=code).first()
        if not plant:
            plant = POSPlant()
            plant.name = code
            plant.corporate_image = corporate_image
            plant.billing_series = bs
            plant.save()

        print("Creando POSZone")
        code = 'zone'
        zone = POSZone.objects.filter(name=code).first()
        if not zone:
            zone = POSZone()
            zone.name = code
            zone.plant = plant
            zone.save()

        print("Creando POS")
        code = 'pos'
        pos = POS.objects.filter(name=code).first()
        if not pos:
            pos = POS()
            pos.name = code
            pos.token = code
            pos.zone = zone
            try:
                pos.save()
            except TypeError:
                pass

        print("Creando POSSlot")
        for code in ['slot', ] + ["slot{}".format(x) for x in range(0, 20)]:
            slot = POSSlot.objects.filter(name=code).first()
            if not slot:
                slot = POSSlot()
                slot.zone = zone
                slot.name = code
                slot.save()

        print("Creando POSProduct")
        POSProduct.objects.all().delete()
        for pf in products:
            pp = POSProduct()
            pp.pos = pos
            pp.product = pf
            pp.save()

        print("Creando Customer")
        customer = Customer.objects.filter(default_customer=True).first()
        if customer is None:
            customer = Customer()
            customer.billing_series = bs
            customer.save()

            person = Person()
            person.customer = customer
            person.name = "Cliente BASE"
            person.save()

            customer.external = person
            customer.save()
