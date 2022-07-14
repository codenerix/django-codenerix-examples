# -*- coding: utf-8 -*-
import datetime
import base64
import io

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext as _
from django.views.generic import View
from django.utils import timezone
from django.core.files import File
from django.conf import settings

from codenerix.helpers import get_template
from codenerix_pos.models import POSHardware

from erp.news.models import News

# from erp.services.models import ServicePerson, ServicePersonDepencents


class Home(View):
    template_name = "home/main.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


@login_required
def home(request):
    template = get_template("home/main", request.user, request.LANGUAGE_CODE)
    output = {}
    output["title"] = _("Home")
    now = datetime.datetime.now()
    output["newss"] = News.objects.filter(
        Q(public=True)
        & Q(language=request.LANGUAGE_CODE)
        & (Q(main_from__isnull=True) | Q(main_from__lte=now))
        & (Q(main_until__isnull=True) | Q(main_until__gte=now))
    ).order_by("-main_from")
    return render(request, template, context=output)


class SlugLevelGet(View):
    def get(self, request, *args, **kwargs):
        slug1 = kwargs["slug1"]
        context = {}
        self.template_name = "base/{}.html".format(slug1)
        return render(request, self.template_name, context)


@login_required
def not_authorized(request):
    return render(request, "base/not_authorized.html")


@login_required
def status(request, status, answer):
    answerjson = urlsafe_base64_decode(answer)
    status = status.lower()
    return HttpResponse(answerjson, status=202 if status == "accept" else 501)


@login_required
def alarms(request):
    json_answer = '{"body": {}, "head": {"total": 0, "order": []}, "meta": {"superuser": true, "permitsuser": "DC"}}'
    return HttpResponse(json_answer, content_type="application/json")


"""
class Signature(View):
    template_name = 'base/signature2.html'

    def get(self, request, *args, **kwargs):
        context = {}
        position = kwargs.get('position', None)
        try:
            position = int(position)
        except Exception:
            position = None

        if position:
            pad = POSHardware.objects.filter(enable=True, kind='SIGN').order_by('pk')
            if pad.count() >= position:
                pad = pad[position-1]
            else:
                raise Http404(_("Uppppss! There are no so many Signature Hardware here!"))
        else:
            pad = POSHardware.objects.filter(enable=True, kind='SIGN').first()
        if pad:
            context['uuid'] = pad.pos.uuid.hex
            context['pos_uuid'] = pad.pos.uuid.hex
            context['pos_key'] = pad.pos.key
        context['files'] = [
            ['title 1', "{}img/codenerix.png".format(settings.STATIC_URL), ],
            ['title 2', "{}img/logo_big.png".format(settings.STATIC_URL), ],
        ]

        # Push host information
        host = request.META.get("HTTP_HOST", None).split(":")[0]
        if host:
            context['websocket_url'] = "{}:{}".format(host, settings.WEBSOCKET_PORT)

        # context['files'] = []
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        signature = request.POST.get('signature', None)
        service_person_pk = request.POST.get('object', None)

        pad = POSHardware.objects.filter(enable=True, kind='SIGN').first()
        if pad:
            context['uuid'] = pad.pos.uuid.hex
            context['pos_uuid'] = pad.pos.uuid.hex
            context['pos_key'] = pad.pos.key
        context['files'] = [
            ['title 1', "{}img/codenerix.png".format(settings.STATIC_URL), ],
            ['title 2', "{}img/logo_big.png".format(settings.STATIC_URL), ],
        ]

        # Push host information
        host = request.META.get("HTTP_HOST", None).split(":")[0]
        if host:
            context['websocket_url'] = "{}:{}".format(host, settings.WEBSOCKET_PORT)

        if signature is None or service_person_pk is None:
            context['error'] = _("Form invalid")
        else:
            service_person = ServicePerson.objects.filter(pk=service_person_pk).first()
            if service_person is None:
                context['error'] = _('Service person invalid')
            else:
                # Prepare file in memory
                filecontent = signature.split(',')[1]
                filecontent = base64.b64decode(filecontent)

                MEM = io.BytesIO()
                MEM.write(filecontent)
                MEM.name = "sign.png"
                MEM.seek(0)

                service_person.signature = File(MEM)

                service_person.save()
                # return redirect("signature")
        return render(request, self.template_name, context)


class Pistolita(View):
    template_name = 'base/pistolita.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}

        barcode = request.POST.get('barcode', None)
        try:
            barcode = int(barcode)
        except ValueError:
            barcode = None

        if barcode:
            spd = ServicePersonDepencents.objects.filter(
                Q(
                    Q(used__isnull=True)
                    | Q(used__isnull=False, used__gte=datetime.datetime.now()-timezone.timedelta(minutes=30))
                ),
                barcode=barcode,
                service_person__date=datetime.datetime.today()
            ).first()
            if spd:
                if spd.used is None:
                    spd.used = datetime.datetime.now()
                    spd.save()
                    context['status'] = 'vending-ok'
                    context['status2'] = 'success'
                    context['message'] = _('Barcode "%(barcode)s" access granted') % {'barcode': barcode}
                else:
                    left = timezone.make_naive(spd.used)-datetime.datetime.now()+timezone.timedelta(minutes=30)
                    minutes = int(left.seconds/60)
                    seconds = left.seconds-minutes*60
                    context['status'] = 'vending-ok2'
                    context['status2'] = 'info'
                    context['message'] = _('Barcode "%(barcode)s" already used') % {'barcode': barcode}
                    context['note'] = _('(%(minutes)s minutes %(seconds)s seconds left)') % {'minutes': minutes, 'seconds': seconds}
            else:
                context['status'] = 'vending-ko'
                context['status2'] = 'danger'
                context['message'] = _('Barcode "%(barcode)s" access denied') % {'barcode': barcode}
        else:
            context['status'] = 'vending-ko'
            context['status2'] = 'danger'
            context['message'] = _('Access denied')

        return render(request, self.template_name, context)
"""
