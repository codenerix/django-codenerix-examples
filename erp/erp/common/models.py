# -*- coding: utf-8 -*-/
import datetime
from django.utils.translation import gettext_lazy as __
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings

from codenerix.models import CodenerixModel
from codenerix_email.models import EmailMessage

LANG_CHOICE = (
    ('es', __('Spanish')),
    ('en', __('English')),
)


class GenModel(CodenerixModel):  # META: Abstract class
    # compatibility
    class Meta(CodenerixModel.Meta):
        abstract = True


class PublicContact(CodenerixModel):
    name = models.CharField(_('Name'), max_length=256, blank=False, null=False)
    last_name = models.CharField(_('Last name'), max_length=256, blank=False, null=False)
    phone = models.CharField(_('Phone'), max_length=256, blank=False, null=False)
    email = models.EmailField(_('Email'), blank=False, null=False)
    subject = models.CharField(_('Subject'), max_length=256, blank=False, null=False)
    body = models.TextField(_('Body'), blank=False, null=False)
    ip = models.GenericIPAddressField(_('IP'), blank=False, null=False, editable=False)
    date = models.DateTimeField(_('Date'), blank=False, null=False, editable=False)
    email_message = models.ManyToManyField(EmailMessage, blank=True, related_name="public_contacts", editable=False)

    def __fields__(self, info):
        fields = []
        fields.append(('date', _('Date')))
        fields.append(('name', _('Name')))
        fields.append(('last_name', _('Last name')))
        fields.append(('phone', _('Phone')))
        fields.append(('email', _('Email')))
        fields.append(('subject', _('Subject')))
        fields.append(('info_message', _('Email Message'), None, 'center'))
        fields.append(('ip', _('IP')))
        # fields.append(('body', _('Body')))
        return fields

    def info_message(self):
        total = self.email_message.count()
        sent = self.email_message.filter(sent=True).count()
        return "{} / {}".format(sent, total)

    def save(self, *args, **kwargs):
        if settings.DEBUG:
            legacy = False
            emails = settings.ADMINS
        else:
            legacy = True
            emails = settings.CLIENTS
        
        message = u'''
Mensaje enviado desde la web {website}:

Nombre: {name}
Apellidos: {last_name}
Teléfono: {phone}
Email: {email}
Asunto: {subject}
Mensage: {body}

--
{name_project} Helper v{version}
        '''.format(
            website=settings.INFO_PROJECT['website'],
            name=self.name,
            last_name=self.last_name,
            phone=self.phone,
            email=self.email,
            subject=self.subject,
            body=self.body,
            version=settings.VERSION,
            name_project=settings.INFO_PROJECT['name_project']
        )
        if self.pk is None:
            self.date = datetime.datetime.now()

        result = super(PublicContact, self).save(*args, **kwargs)

        for name, email in emails:
            email_message = EmailMessage()
            email_message.efrom = settings.DEFAULT_FROM_EMAIL
            email_message.eto = email
            email_message.subject = "[{}] {}".format(settings.INFO_PROJECT['name_project'], _(' Formulario de contacto'))
            email_message.body = message
            email_message.save()
            email_message.send(legacy=legacy, silent=True)
            self.email_message.add(email_message)

        return result
