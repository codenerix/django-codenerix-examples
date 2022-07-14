# -*- coding: utf-8 -*-
import json
from django.db.models import Q
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import View
from django.conf import settings

from codenerix.views import (
    GenList,
    GenCreate,
    GenCreateModal,
    GenUpdate,
    GenUpdateModal,
    GenDelete,
    GenDetail,
    GenDetailModal,
)
from codenerix.multiforms import MultiForm

from erp.transports.models import TransportZone, TransportRate, MODELS_TRANSPORT
from erp.transports.forms import TransportZoneForm, TransportRateForm

# from codenerix_transports.models import TRANSPORT_PROTOCOL_CHOICES
from codenerix_geodata.models import Country, Region, Province, City

formsfull = {}
for info in MODELS_TRANSPORT:
    field = info[0]
    model = info[1]
    formsfull[model] = [(None, None, None)]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "from erp.transports.models import {}Text{}\n".format(model, lang_code)
        query += "from erp.transports.forms import {}TextForm{}".format(
            model, lang_code
        )
        exec(query)

        formsfull[model].append(
            (eval("{}TextForm{}".format(model, lang_code.upper())), field, None)
        )


# ###########################################
# TransportZone
class TransportZoneList(GenList):
    model = TransportZone
    extra_context = {
        "menu": ["transport", "transport_zone"],
        "bread": [_("Transport"), _("TransportZone")],
    }


class TransportZoneCreate(MultiForm, GenCreate):
    model = TransportZone
    form_class = TransportZoneForm
    forms = formsfull["TransportZone"]


class TransportZoneCreateModal(GenCreateModal, TransportZoneCreate):
    pass


class TransportZoneUpdate(MultiForm, GenUpdate):
    model = TransportZone
    form_class = TransportZoneForm
    forms = formsfull["TransportZone"]


class TransportZoneUpdateModal(GenUpdateModal, TransportZoneUpdate):
    pass


class TransportZoneDelete(GenDelete):
    model = TransportZone


class TransportZoneSubList(GenList):
    model = TransportZone
    extra_context = {
        "menu": ["transport", "transport_zone"],
        "bread": [_("Transport"), _("TransportZone")],
    }

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get("pk", None)
        limit["link"] = Q(xxxxxxx__pk=pk)
        return limit


class TransportZoneDetails(GenDetail):
    model = TransportZone
    groups = TransportZoneForm.__groups_details__()


class TransportZoneDetailModal(GenDetailModal, TransportZoneDetails):
    pass


# ###########################################
# TransportRate
class TransportRateList(GenList):
    model = TransportRate
    extra_context = {
        "menu": ["transport", "transport_rate"],
        "bread": [_("Transport"), _("TransportRate")],
    }


class TransportRateCreate(MultiForm, GenCreate):
    model = TransportRate
    form_class = TransportRateForm
    forms = formsfull["TransportRate"]


class TransportRateCreateModal(GenCreateModal, TransportRateCreate):
    pass


class TransportRateUpdate(MultiForm, GenUpdate):
    model = TransportRate
    form_class = TransportRateForm
    forms = formsfull["TransportRate"]


class TransportRateUpdateModal(GenUpdateModal, TransportRateUpdate):
    pass


class TransportRateDelete(GenDelete):
    model = TransportRate


class TransportRateSubList(GenList):
    model = TransportRate
    extra_context = {
        "menu": ["transport", "transport_rate"],
        "bread": [_("Transport"), _("TransportRate")],
    }

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get("pk", None)
        limit["link"] = Q(xxxxxxx__pk=pk)
        return limit


class TransportRateDetails(GenDetail):
    model = TransportRate
    groups = TransportRateForm.__groups_details__()


class TransportRateDetailModal(GenDetailModal, TransportRateDetails):
    pass


class TransportCalculate(View):
    @staticmethod
    def calculator(POST, VAT=1.0):

        context = {}
        error = None

        country = POST.get("country", None)
        region = POST.get("region", None)
        province = POST.get("province", None)
        city = POST.get("city", None)
        zipcode = POST.get("zipcode", None)

        try:
            weight = float(POST.get("weight", None).replace(",", "."))
        except Exception:
            weight = None

        region = get_region(zipcode)
        if region is None:
            error = _("Zipcode invalid")
        else:
            if isinstance(region, Region):
                # region is a Region
                country = None
                region = region.pk
                province = None
                city = None
            elif isinstance(region, Country):
                # region is a Country
                country = region.pk
                region = None
                province = None
                city = None
            else:
                try:
                    if country:
                        country = int(country)
                    if region:
                        region = int(region)
                    if province:
                        province = int(province)
                    if city:
                        city = int(city)
                except ValueError:
                    error = _("Parameters invalid")

        if error is not None:
            context["error"] = error
        elif weight is None:
            context["error"] = _("Weight invalid!")
        else:
            context["error"] = None
            rates = None
            if city:
                rates = TransportRate.objects.filter(
                    weight__gt=weight, zone__city__pk=city
                ).order_by("weight")
            if not rates and province:
                rates = TransportRate.objects.filter(
                    weight__gt=weight,
                    zone__province__pk=province,
                    zone__city__isnull=True,
                ).order_by("weight")
            if not rates and region:
                rates = TransportRate.objects.filter(
                    weight__gt=weight,
                    zone__region__pk=region,
                    zone__city__isnull=True,
                    zone__province__isnull=True,
                ).order_by("weight")
            if not rates and country:
                rates = TransportRate.objects.filter(
                    weight__gt=weight,
                    zone__country__pk=country,
                    zone__city__isnull=True,
                    zone__province__isnull=True,
                    zone__region__isnull=True,
                ).order_by("weight")

            tmp = {}
            list_protocol_config = list(settings.TRANSPORTS.keys())
            list_protocol_used = []
            if rates:
                for rate in rates:
                    if (
                        rate.protocol not in tmp
                        and rate.protocol in list_protocol_config
                    ):
                        tmp[rate.protocol] = {
                            "weight": rate.weight,
                            "price": rate.price_transport * VAT,
                        }
                        list_protocol_used.append(rate.protocol)

            cities = {}
            # provinces = {}
            # regions = {}
            countries = {}
            i = 0
            for protocol in list_protocol_config:
                i += 1
                if (
                    protocol != "meta"
                    and protocol not in list_protocol_used
                    and settings.TRANSPORTS[protocol]["protocol"] != "dummy"
                ):
                    for rule in settings.TRANSPORTS[protocol]["logic"]:
                        if "weight" in rule and "price" in rule:
                            try:
                                logic_weight = float(rule["weight"])
                                logic_price = float(rule["price"])
                            except ValueError:
                                logic_weight = None
                                logic_price = None
                            if logic_weight and logic_price:
                                # city
                                if (
                                    "lang" in settings.TRANSPORTS[protocol]
                                    and "city" in rule
                                    and city
                                    and "province" in rule
                                    and "region" in rule
                                    and "country" in rule
                                ):
                                    if rule["city"] not in cities:
                                        logic_city = City.objects.filter(
                                            **{
                                                "{}__name".format(
                                                    settings.TRANSPORTS[protocol][
                                                        "lang"
                                                    ]
                                                ): rule["city"],
                                                "province__code": rule["province"],
                                                "region__code": rule["region"],
                                                "region__country__code": rule[
                                                    "country"
                                                ],
                                            }
                                        ).first()
                                        cities[rule["city"]] = logic_city
                                    else:
                                        logic_city = cities[rule["city"]]
                                    if logic_city:
                                        if logic_city.pk == city:
                                            if (
                                                protocol in tmp
                                                and tmp[protocol]
                                                and tmp[protocol]["weight"]
                                                > logic_weight
                                            ):
                                                tmp[protocol] = {
                                                    "city": city,
                                                    "weight": logic_weight,
                                                    "price": logic_price,
                                                }
                                            else:
                                                tmp[protocol] = {
                                                    "city": city,
                                                    "weight": logic_weight,
                                                    "price": logic_price,
                                                }
                                # province
                                if (
                                    "city" not in rule
                                    and "province" in rule
                                    and province
                                    and "region" in rule
                                    and "country" in rule
                                ):
                                    if (
                                        protocol not in tmp
                                        or "city" not in tmp[protocol]
                                    ):
                                        logic_province = Province.objects.filter(
                                            code=rule["province"],
                                            region__code=rule["region"],
                                            region__country__code=rule["country"],
                                        ).first()
                                        if logic_province:
                                            if logic_province.pk == province:
                                                if (
                                                    protocol in tmp
                                                    and [protocol]["weight"]
                                                    > logic_weight
                                                ):
                                                    tmp[protocol] = {
                                                        "province": province,
                                                        "weight": logic_weight,
                                                        "price": logic_price,
                                                    }
                                                else:
                                                    tmp[protocol] = {
                                                        "province": province,
                                                        "weight": logic_weight,
                                                        "price": logic_price,
                                                    }
                                # region
                                if (
                                    "city" not in rule
                                    and "province" not in rule
                                    and "region" in rule
                                    and region
                                    and "country" in rule
                                    and country
                                ):
                                    if protocol not in tmp or (
                                        "city" not in tmp[protocol]
                                        and "province" not in tmp[protocol]
                                    ):
                                        logic_region = Region.objects.filter(
                                            code=rule["region"],
                                            country__code=rule["country"],
                                        ).first()
                                        if logic_region:
                                            if logic_region.pk == region:
                                                if (
                                                    protocol in tmp
                                                    and tmp[protocol]
                                                    and tmp[protocol]["weight"]
                                                    > logic_weight
                                                ):
                                                    tmp[protocol] = {
                                                        "region": region,
                                                        "weight": logic_weight,
                                                        "price": logic_price,
                                                    }
                                                else:
                                                    tmp[protocol] = {
                                                        "region": region,
                                                        "weight": logic_weight,
                                                        "price": logic_price,
                                                    }
                                # country
                                if (
                                    "city" not in rule
                                    and "province" not in rule
                                    and "region" not in rule
                                    and "country" in rule
                                    and country
                                ):
                                    if protocol not in tmp or (
                                        "city" not in tmp[protocol]
                                        and "province" not in tmp[protocol]
                                        and "region" not in tmp[protocol]
                                    ):
                                        if rule["country"] not in countries:
                                            logic_country = Country.objects.filter(
                                                code=rule["country"]
                                            ).first()
                                            countries[rule["country"]] = logic_country
                                        else:
                                            logic_country = countries[rule["country"]]
                                        if logic_country:
                                            if logic_country.pk == country:
                                                if (
                                                    protocol in tmp
                                                    and tmp[protocol]
                                                    and tmp[protocol]["weight"]
                                                    > logic_weight
                                                ):
                                                    tmp[protocol] = {
                                                        "country": country,
                                                        "weight": logic_weight,
                                                        "price": logic_price,
                                                    }
                                                else:
                                                    tmp[protocol] = {
                                                        "country": country,
                                                        "weight": logic_weight,
                                                        "price": logic_price,
                                                    }

            if tmp:
                context["rates"] = tmp
            else:
                context["rates"] = None

        return context

    def get(self, request, *args, **kwargs):
        POST = json.loads(request.GET.get("json"))
        context = TransportCalculate.calculator(POST, 1.21)
        return JsonResponse(context)


def get_region(zipcode):
    if len(zipcode) == 5:
        try:
            zp = str(int(zipcode))[0:2]
        except ValueError:
            zp = None

        spain = Country.objects.get(code="ES")
        if zp is None:
            region = None
        elif zp == "35" or zp == "38":  # CANARIAS
            region = Region.objects.get(code="CN", country=spain)
        elif zp == "07":  # BALEARES
            region = Region.objects.get(code="IB", country=spain)
        elif zp == "51":  # CEUTA
            region = Region.objects.get(code="CE", country=spain)
        elif zp == "52":  # MELILLA
            region = Region.objects.get(code="ML", country=spain)
        else:  # PENINSULA
            region = spain
    else:
        region = None

    return region
