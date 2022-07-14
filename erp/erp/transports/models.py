# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from codenerix.models import CodenerixModel
from codenerix_extensions.helpers import get_language_database
from codenerix_geodata.models import Country, Region, Province, City
from codenerix_transports.models import TRANSPORT_PROTOCOL_CHOICES


class GenTransportText(CodenerixModel):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True

    name = models.CharField(_("Name"), max_length=70, blank=False, null=False)

    def __str__(self):
        return u"{}".format(smart_str(self.name))

    def __unicode__(self):
        return self.__str__()


class TransportZone(CodenerixModel):
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, blank=True, null=True, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, blank=True, null=True, on_delete=models.CASCADE)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        lang = get_language_database()
        lang_model = getattr(self, '{}'.format(lang), None)
        if lang_model:
            name = u"{}".format(smart_str(lang_model.name))
        else:
            name = u"{}".format(smart_str(self.country), smart_str(self.region), smart_str(self.province), smart_str(self.city))
        return name

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('country', _('Country')))
        fields.append(('region', _('Region')))
        fields.append(('province', _('Province')))
        fields.append(('city', _('City')))
        return fields


class TransportRate(CodenerixModel):
    zone = models.ForeignKey(TransportZone, blank=False, null=True, default=None, on_delete=models.CASCADE)
    protocol = models.CharField(_('Protocol'), choices=TRANSPORT_PROTOCOL_CHOICES, max_length=10, blank=False, null=False)
    price_transport = models.FloatField(_('Price of transport'), blank=False, null=False)
    weight = models.FloatField(_('Weight grams max'), blank=False, null=False)

    def __str__(self):
        lang = get_language_database()
        lang_model = getattr(self, '{}'.format(lang), None)
        if lang_model:
            name = u"{}".format(smart_str(lang_model.name))
        else:
            name = u"{}".format(smart_str(self.zone), smart_str(self.protocol), smart_str(self.price_transport), smart_str(self.weight))
        return name

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('zone', _('Zone')))
        fields.append(('protocol', _('Protocol')))
        fields.append(('price_transport', _('Price of transport')))
        fields.append(('weight', _('Weight max')))
        return fields


MODELS_TRANSPORT = [
    ('transport_zone', 'TransportZone'),
    ('transport_rate', 'TransportRate'),
]

for info in MODELS_TRANSPORT:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "class {}Text{}(GenTransportText):\n".format(model, lang_code)
        query += "  {} = models.OneToOneField({}, blank=False, null=False, related_name='{}', on_delete=models.CASCADE)\n".format(field, model, lang_code.lower())
        exec(query)
