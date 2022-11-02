# -*- coding: utf-8 -*-

# Django
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.translation import gettext as _

# Codenerix
from codenerix.views import (
    GenList,
    GenCreate,
    GenDetail,
    GenUpdate,
    GenDelete,
)

# Models
from basic.base.models import Info

# Forms
from basic.base.forms import InfoForm


@login_required
def alarms(request):
    return JsonResponse(
        {
            "body": {},
            "head": {
                "total": 0,
                "order": [],
            },
            "meta": {
                "superuser": True,
                "permitsuser": "DC",
            },
        }
    )


class InfoList(GenList):
    model = Info
    show_details = True


class InfoCreate(GenCreate):
    model = Info
    form_class = InfoForm


class InfoDetail(GenDetail):
    model = Info
    groups = [
        (
            _("Info"),
            12,
            ["info", 12, None, None, "right"],
        )
    ]


class InfoEdit(GenUpdate):
    model = Info
    form_class = InfoForm


class InfoDelete(GenDelete):
    model = Info


class InfoList2(GenList):
    model = Info
    modelname = "info2"
    show_details = True


class InfoCreate2(GenCreate):
    model = Info
    form_class = InfoForm


class InfoDetail2(GenDetail):
    model = Info
    groups = [
        (
            _("Info"),
            12,
            ["info", 12, None, None, "right"],
        )
    ]


class InfoEdit2(GenUpdate):
    model = Info
    form_class = InfoForm


class InfoDelete2(GenDelete):
    model = Info


class InfoList3(InfoList):
    modelname = "info3"


class InfoCreate3(InfoCreate):
    pass


class InfoDetail3(InfoDetail):
    pass


class InfoEdit3(InfoEdit):
    pass


class InfoDelete3(InfoDelete):
    pass
