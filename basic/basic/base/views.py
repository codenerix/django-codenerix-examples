# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

# Django
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.forms.utils import ErrorList
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _

# Codenerix
from codenerix.helpers import get_template
from codenerix.views import (
    GenList,
    GenCreate,
    GenCreateModal,
    GenDetail,
    GenUpdate,
    GenUpdateModal,
    GenDelete,
    GenForeignKey,
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
