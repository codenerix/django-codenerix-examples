# -*- coding: utf-8 -*-
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail
from codenerix.helpers import get_client_ip
from codenerix_extensions.helpers import get_language_database

from .models import PublicContact
from .forms import PublicContactForm

from erp.common.helpers import get_menu


# PublicContact
class PublicContactList(GenList):
    model = PublicContact
    show_details = True
    extra_context = {
        'menu': ['common', 'public_contact'],
        'bread': [_('People'), _('PublicContact')]
    }
    linkadd = False
    default_ordering = ['-date', ]
    onlybase = True


class PublicContactCreate(GenCreate):
    model = PublicContact
    form_class = PublicContactForm
    public = True
    linkdelete = False
    linkback = False
    linksavenew = False
    linksavehere = False
    hide_foreignkey_button = True
    title = _('Contact')
    show_internal_name = False
    gentranslate = {
        'Save': _('Send')
    }
    buttons_top = False

    def form_valid(self, form):
        ip = get_client_ip(self.request)
        form.instance.ip = ip
        return super(PublicContactCreate, self).form_valid(form)


class PublicContactCreateModal(GenCreateModal, PublicContactCreate):
    pass


class PublicContactUpdate(GenUpdate):
    model = PublicContact
    form_class = PublicContactForm


class PublicContactUpdateModal(GenUpdateModal, PublicContactUpdate):
    pass


class PublicContactDelete(GenDelete):
    model = PublicContact


class PublicContactDetails(GenDetail):
    model = PublicContact
    groups = PublicContactForm.__groups_details__()


class PublicContactFrontend(GenList):
    model = PublicContact
    show_details = False
    extra_context = {
        'menu': ['common', 'public_contact'],
        'bread': [_('People'), _('PublicContact')]
    }
    public = True

    extends_base = "frontend/contact_form.html"
    # extends_base = "frontend/backend_user.html"

    def __limitQ__(self, info):
        limit = {}
        limit['file_link'] = Q(pk=-1)
        return limit

    def dispatch(self, *args, **kwargs):
        lang = get_language_database()
        self.extra_context['menu'] = get_menu(lang)
        return super(PublicContactFrontend, self).dispatch(*args, **kwargs)
