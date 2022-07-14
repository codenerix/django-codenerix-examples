# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand

from codenerix.lib.debugger import Debugger
from erp.common.helpers import PaymentMethod


class Command(BaseCommand, Debugger):
    def handle(self, *args, **options):
        pay = PaymentMethod()
        print pay.get_currency()
        info_pr = pay.pay('sabadell', 'search', 123, 1)
        print info_pr
        if not info_pr['error']:
            pr = info_pr['payment_request']
            print pr
            print "_______________________"
            print pr.get_approval()
