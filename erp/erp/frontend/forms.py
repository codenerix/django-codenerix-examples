# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import gettext as _

from codenerix.forms import GenModelForm, GenForm
# from codenerix_invoicing.models_sales import SalesOrder
from codenerix_extensions.validators import spanishNIFNIECIF

from erp.people.models import DOCUMENT_TYPES

class OrderForm(GenModelForm):
    pass
"""
class OrderForm_XXX(GenModelForm):
    class Meta:
        model = SalesOrder
        fields = []

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

    def __groups__(self):
        return []

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['code', 6],
                ['date', 6],
                ['status_order', 6],
                ['observations', 6],
            ), (
                _('Total'), 12,
                ['subtotal', 6],
                ['discounts', 6],
                ['taxes', 6],
                ['total', 6],
            )
        ]
        return g
"""

class RequestInvoiceForm(GenForm):
    nid = forms.CharField(label=_("NID"), max_length=20, required=True, validators=[spanishNIFNIECIF])
    nid_type = forms.ChoiceField(label=_("NID Type"), choices=DOCUMENT_TYPES)
    name = forms.CharField(label=_("Name"), max_length=45, required=True)
    surname = forms.CharField(label=_("Surname"), max_length=90, required=True)
    legal = forms.BooleanField(
        label=_("Confirmo que los datos son correctos"),
        required=True
    )
    """
    status = forms.ModelChoiceField(label=_("Status"), queryset=PermissionStatus.objects.all(),required=True)
    note = forms.CharField(label=_("Note"),widget=forms.Textarea(attrs={'rows': 2, 'cols': 25}), required=False)
    handler = forms.ModelChoiceField(label=_("Handler"),queryset=HandlingPrice.objects.all(),required=False)
    kind = forms.ModelChoiceField(label=_("Kind"),queryset=NotificationKind.objects.all(),required=False)
    public = forms.BooleanField(label=_("Public"),required=False)
    list_email = MultiEmailField(label=_("Emails"),required=False)
    description = forms.CharField(label=_("Description"),widget=forms.Textarea(attrs={'rows': 6, 'cols': 25}), required=False)
    """
    @staticmethod
    def __groups__():
        g = [
            (
                _('Information'), 12,
                ['name', 6],
                ['surname', 6],
                ['nid', 4],
                ['nid_type', 4],
                ['legal', 4],
            )
        ]
        return g
