# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import gettext_lazy as _

from codenerix.forms import GenModelForm
from codenerix.fields import GenReCaptchaField

from .models import PublicContact


class PublicContactForm(GenModelForm):
    legal = forms.BooleanField(
        label=_("Acepto los <a href='/terminos-de-uso' target='_blank'>terminos</a>"),
        required=True
    )
    recaptcha = GenReCaptchaField('recaptcha')

    class Meta:
        model = PublicContact
        exclude = []

    def __groups__(self):
        return [
            (
                _(u'Contact'), 12,
                ['name', 6],
                ['last_name', 6],
                ['phone', 6],
                ['email', 6],
                ['subject', 12],
                ['body', 12],
                ['legal', 3],
            ), (
                _(u'Code secure'), 12,
                ['recaptcha', 6],
            )
        ]

    @staticmethod
    def __groups_details__():
        return [
            (
                _(u'Details'), 12,
                ['name', 6],
                ['last_name', 6],
                ['phone', 6],
                ['email', 12],
                ['subject', 12],
                ['body', 12],
            )
        ]
