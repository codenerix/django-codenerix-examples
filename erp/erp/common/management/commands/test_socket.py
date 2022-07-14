import json
from django.core.management.base import BaseCommand
from django.conf import settings

from codenerix.lib.debugger import Debugger
from codenerix_pos.models import *
from urbangest.services.models import ServicePerson


class Command(BaseCommand, Debugger):

    def handle(self, *args, **options):
        tablet = POSHardware.objects.filter(kind=KIND_POSHARDWARE_SIGN).first()
        # pos = tablet.pos
        # pos = POS.objects.last()
        """
        print pos
        print pos.send('hola', uid=pos.uuid)
        print pos.send('hola', uid=tablet.uuid)
        print pos.send({'action': 'get_config'})
        print "___________"
        print pos.send({'action': 'ping'}, uid=tablet.uuid)
        """
        # print pos.send({'action': 'ping'})
        # print pos.send({'asd': '456'})
        print "___________"
        # print tablet.uuid

        info = []
        service_person = ServicePerson.objects.get(pk=16)
        for person in service_person.servicepersondependents.all():
            color = get_color(person.service_day.color_service)
            info.append({
                'person': person.dependent.__str__(),
                'service': person.service_day.service.product_final.es.name,
                'hour': person.service_day.hour.__str__(),
                'color': color
            })

        print tablet.send({'action': 'msg', 'info': json.dumps(info)})


def get_color(color):
    if color == 'R':
        code = 'red'
    elif color == 'Y':
        code = 'yellow'
    elif color == 'G':
        code = 'green'
    elif color == 'B':
        code = 'blue'
    return code
