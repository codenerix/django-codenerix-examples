# -*- coding: utf-8 -*-
from django.utils.translation import gettext as _

from codenerix.forms import GenModelForm

from exchange.base.models import Currency, Exchange


class CurrencyForm(GenModelForm):

    class Meta:
        model = Currency
        exclude = []

    def __groups__(self):
        return [
            (
                _("Info"), 12,
                ['name', 4],
                ['symbol', 4],
                ['iso4217', 4],
            ),
        ]


class ExchangeForm(GenModelForm):

    class Meta:
        model = Exchange
        exclude = []
        autofill = {
            'sell_currency': ['select', 3, 'currency_foreign', 'buy_currency'],
            'buy_currency': ['select', 3, 'currency_foreign', 'sell_currency'],
        }

    def __init__(self, *args, **kwargs):
        super(ExchangeForm, self).__init__(*args, **kwargs)
        self.fields['rate'].widget.attrs['disabled'] = True
        self.fields['buy_amount'].widget.attrs['disabled'] = True

    def clean_rate(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.rate
        else:
            return self.cleaned_data['rate']

    def clean_buy_amount(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.buy_amount
        else:
            return self.cleaned_data['buy_amount']

    def __groups__(self):
        return [(
            _('Sell'), 4,
            ['sell_currency', 12, None, None, None, None, None, ['ng-change=amount_update()']],
            ['sell_amount', 12, None, None, None, None, None, ['ng-change=amount_update()']],
        ), (
            _('Rate'), 4,
            ['rate', 12],
        ), (
            _('Buy'), 4,
            ['buy_currency', 12, None, None, None, None, None, ['ng-change=amount_update()']],
            ['buy_amount', 12],
        ), ]

    @staticmethod
    def __groups_details__():
        return [
            (
                _('Control'), 4,
                ['cid', 6],
                ['owner', 6],
                ['created', 12],
            ),
            (
                _('Rate'), 8,
                ['sell_currency', 6],
                ['sell_amount', 6],
                ['buy_currency', 6],
                ['buy_amount', 6],
                ['rate', 12],
            ),
        ]
