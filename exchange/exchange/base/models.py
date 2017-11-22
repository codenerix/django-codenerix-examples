# -*- coding: utf-8 -*-

import random
import requests

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import smart_text
from django.db import models

from codenerix.helpers import CodenerixEncoder
from codenerix.models import CodenerixModel
from codenerix.middleware import get_current_user


class Currency(CodenerixModel):
    '''
    Currencies
    '''
    name = models.CharField(_('Name'), max_length=15, blank=False, null=False, unique=True)
    symbol = models.CharField(_('Symbol'), max_length=2, blank=False, null=False, unique=True)
    iso4217 = models.CharField(_('ISO 4217 Code'), max_length=3, blank=False, null=False, unique=True)
    
    def __str__(self):
        return u"{0} ({1})".format(smart_text(self.name), smart_text(self.symbol))
    
    def __fields__(self,info):
        fields=[]
        fields.append(('name',_('Name'),100))
        fields.append(('symbol',_('Symbol'),100))
        return fields
    
    def rate(self, buy):
        # Prepare the call
        url = "http://api.fixer.io/latest"
        payload = {'base':self.iso4217, 'symbols':buy.iso4217}
        r = requests.get(url, params=payload)
        r.raise_for_status()
        # Read the answer
        data = r.json()
        rate = data['rates'][buy.iso4217]
        return rate
        
    class Meta:
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')


class Exchange(CodenerixModel):
    cid = models.CharField(verbose_name=_('ID'), max_length=9, unique=True, editable=False)
    sell_currency = models.ForeignKey(Currency, verbose_name=_('Sell Currency'), related_name='exchanges_sell')
    sell_amount = models.FloatField(_('Sell Amount'), blank=False, null=False)
    buy_currency = models.ForeignKey(Currency, verbose_name=_('Buy Currency'), related_name='exchanges_buy')
    buy_amount = models.FloatField(_('Buy Amount'), blank=False, null=False)
    rate = models.FloatField(_('Rate'), blank=False, null=False)
    owner = models.ForeignKey(User, verbose_name=_('Titular'), related_name='contacts', editable=False)

    def __fields__(self, info):
        return (
            ('cid', _('ID')),
            ('sell_currency', _('Sell')),
            ('sell_amount', _('Sell')),
            ('buy_currency', _('Buy')),
            ('buy_amount', _('Buy')),
            ('rate', _('Rate')),
            ('created', _('Booked')),
        )

    def __searchQ__(self, info, text):
        return {
            'cid': models.Q(cid__icontains=text),
            'sell_currency': models.Q(sell_currency__name__icontains=text),
            'sell_currency': models.Q(sell_currency__symbol__icontains=text),
            'sell_currency': models.Q(sell_currency__iso4217__icontains=text),
            'sell_amount': models.Q(sell_amount__icontains=text),
            'buy_currency': models.Q(buy_currency__name__icontains=text),
            'buy_currency': models.Q(buy_currency__symbol__icontains=text),
            'buy_currency': models.Q(buy_currency__iso4217__icontains=text),
            'buy_amount': models.Q(buy_amount__icontains=text),
            'rate': models.Q(rate__icontains=text),
            'owner': models.Q(owner__username__icontains=text),
            'owner': models.Q(owner__first_name__icontains=text),
            'owner': models.Q(owner__last_name__icontains=text),
            'created': 'datetime',
        }
    
    def __str__(self):
        return self.cid
    
    def save(self, *args, **kwards):
        # If we are creating
        if not self.pk:
            # Set a new CID dynamically
            self.cid = str(random.randint(0,999999999))
            # Try to get the user
            user = get_current_user()
            # Set the owner to the current user
            if user:
                self.owner = user
        
        # Get rate on realtime (to avoid user decision delay)
        self.rate = self.sell_currency.rate(self.buy_currency)
        # Recalculate amount
        self.buy_amount = self.rate * self.sell_amount
        
        # Keep going like usually
        return super(Exchange, self).save(*args, **kwards)
    
    class Meta:
        verbose_name = _('exchange')
        verbose_name_plural = _('exchanges')


# Method for updating saved exchanges if they don't have CID yet
@receiver(post_save, sender=Exchange, dispatch_uid="update_exchange_cid")
def update_exchange(sender, instance, **kwargs):
    # If this instance doesn't have CID yet
    if instance.cid[0]!='T':
        # Create a new CID with CodenerixEncoder
        enc = CodenerixEncoder()
        cid = enc.numeric_encode(instance.pk,dic='alphanum',length=7)
        # Set the new CID and save
        instance.cid = "TR{:>07s}".format(cid)
        instance.save()


