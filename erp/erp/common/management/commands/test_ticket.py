# -*- coding: utf-8 -*-
import base64
from django.core.management.base import BaseCommand  # , CommandError

from codenerix_invoicing.models_sales import SalesBasket
from codenerix_lib.debugger import Debugger


class Command(BaseCommand, Debugger):

    def handle(self, *args, **options):
        basket = SalesBasket.objects.last()
        msg = []
        F = open("/home/jsoler/zonaprog/urbangest/base/urbangest/common/management/commands/Icono.png", "rb")
        logo = base64.b64encode(F.read())
        msg.append(['i', logo])
        msg.append(['t', "Codigo: {}".format(basket.code)])
        msg.append(['t', "Fecha: {}".format(basket.date)])
        msg.append(['t', "---------"])
        msg.append(['t', "{}\t{}\t{}\t{}".format("quantity", "product", "price", "total")])
        msg.append(['t', "---------"])
        for line in basket.line_basket_sales.all():
            msg.append(['t', u"{}\t{}\t{}€\t{}€".format(line.quantity, line.product, line.price, (line.price * line.quantity))])
        msg.append(['t', "---------"])
        prices = basket.calculate_price_doc()
        print prices
        msg.append(['t', u"{}\t\t\t{}€".format('Subtotal', prices['subtotal'])])
        for tax in prices['taxes']:
            msg.append(['t', u"{}\t\t\t\t{}€".format(tax, prices['taxes'][tax])])
        for discount in prices['discounts']:
            msg.append(['t', u"{}\t\t\t\t{}€".format(discount, prices['discounts'][discount])])

        msg.append(['t', u"{}\t\t\t\t{}€".format('Total', prices['total'])])
        msg.append(['t', "---------"])
        msg.append(['b', basket.code])
        msg.append(['t', "\r"])

        for m in msg:
            print u"{}\t{}".format(m[0], m[1])

        print ""
