from django.core.management.base import BaseCommand

from codenerix_lib.debugger import Debugger
from codenerix_products.models import ProductUnique

from codenerix_invoicing.models_sales import (
    SalesLines,
    SalesBasket,
    SalesOrder,
    SalesTicket,
    SalesAlbaran,
    SalesInvoice,
)
from codenerix_invoicing.models_sales import Customer, ROLE_BASKET_BUDGET


class Command(BaseCommand, Debugger):
    def handle(self, *args, **options):
        # Set debugger
        self.set_debug()
        self.set_name("CLEAR SALES!!!")
        self.debug("Init", color="blue")

        self.debug("Remove stock locked", color="cyan")
        for pu in ProductUnique.objects.all():
            pu.stock_locked = 0
            pu.save()

        self.debug("Remove models!!", color="cyan")
        for m in [
            SalesLines,
            SalesBasket,
            SalesOrder,
            SalesTicket,
            SalesAlbaran,
            SalesInvoice,
        ]:
            m.objects.all().delete()

        self.debug("Creating budget!!", color="red")
        b = SalesBasket()
        b.customer = Customer.objects.first()
        b.role = ROLE_BASKET_BUDGET
        b.signed = True
        b.name = "test"
        b.save()

        self.debug("End", color="blue")
