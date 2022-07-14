# -*- coding: utf-8 -*-
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from codenerix.forms import GenModelForm

from erp.transports.models import TransportZone, TransportRate, MODELS_TRANSPORT


class TransportZoneForm(GenModelForm):
    class Meta:
        model = TransportZone
        exclude = []
        autofill = {
            'TransportZoneForm_country': ['select', 3, 'CDNX_ext_location_country_foreign', ],
            'TransportZoneForm_region': ['select', 3, 'CDNX_ext_location_regions_foreign', 'country:TransportZoneForm_country', ],
            'TransportZoneForm_province': ['select', 3, 'CDNX_ext_location_provinces_foreign', 'region:TransportZoneForm_region', ],
            'TransportZoneForm_city': ['select', 3, 'CDNX_ext_location_citys_foreign', 'province:TransportZoneForm_province', ],
        }

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['country', 6],
                ['region', 6],
                ['province', 6],
                ['city', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['country', 6],
                ['region', 6],
                ['province', 6],
                ['city', 6],
            )
        ]
        return g


class TransportRateForm(GenModelForm):
    class Meta:
        model = TransportRate
        exclude = []

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['zone', 6],
                ['protocol', 6],
                ['price_transport', 6],
                ['weight', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['zone', 6],
                ['protocol', 6],
                ['price_transport', 6],
                ['weight', 6],
            )
        ]
        return g


for info in MODELS_TRANSPORT:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "from erp.transports.models import {}Text{}\n".format(model, lang_code)
        exec(query)
        query = """
class {model}TextForm{lang}(GenModelForm):\n
    class Meta:\n
        model={model}Text{lang}\n
        exclude = []\n
    def __groups__(self):\n
        return [(_('Details'),12,"""
        if lang_code == settings.LANGUAGES_DATABASES[0]:
            query += """
                ['name', 12, None, None, None, None, None, ["ng-blur=refresh_lang_field('name', '{model}TextForm', [{languages}])"]],
            )]\n"""
        else:
            query += """
                ['name', 12],
            )]\n"""

        exec(query.format(model=model, lang=lang_code, languages="'{}'".format("','".join(settings.LANGUAGES_DATABASES))))
