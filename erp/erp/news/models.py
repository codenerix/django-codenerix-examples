# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _
from django.utils.encoding import smart_str

from erp.common.models import GenModel, LANG_CHOICE


class News(GenModel):
    '''
    News
    '''
    
    title = models.CharField(_("title"), max_length=150, blank=False, null=False)
    subtitle = models.CharField(_("subtitle"), max_length=150, blank=True, null=True)
    content = models.TextField(_("content"), blank=False, null=False)
    web_from = models.DateTimeField(_("show in web page from"), blank=False, null=False)
    web_until = models.DateTimeField(_("show in web page until"), blank=True, null=True)
    main_from = models.DateTimeField(_("show in main page from"), blank=False, null=False)
    main_until = models.DateTimeField(_("show in main page until"), blank=False, null=False)
    public = models.BooleanField(_("public"), blank=False, null=False, default=False)
    language = models.CharField(_("language"), max_length=10, choices=LANG_CHOICE, blank=False, null=False)
    
    def __unicode__(self):
        return smart_str(self.title)
    
    def __fields__(self, info):
        fields = []
        if info.profile == 'admin':
            fields.append(('title', _('Title')))
            fields.append(('subtitle', _('Subtitle')))
            fields.append(('web_from', _('Web from')))
            fields.append(('web_until', _('Web until')))
            fields.append(('main_from', _('Main from')))
            fields.append(('main_until', _('Main until')))
            fields.append(('public', _('Public?')))
            fields.append(('language', _('Language')))
        else:
            fields.append(('web_from', _('Web from')))
            fields.append(('title', _('Title')))
            fields.append(('subtitle', _('Subtitle')))
            fields.append(('content', _('Content')))
        return fields
    
    def __limitQ__(self, info):
        limit = {}
        if info.profile != 'admin':
            limit['public'] = Q(public=True)
            limit['language'] = Q(language=info.request.LANGUAGE_CODE)
        return limit
    
    def __searchQ__(self, text, info):
        s = {}
        s['title'] = Q(title__icontains=text)
        s['subtitle'] = Q(subtitle__icontains=text)
        s['content'] = Q(content__icontains=text)
        s['web_from'] = "datetime"
        return s
    
    def __searchF__(self, info):
        # Build field structure
        tf = {}
        if info.profile == 'admin':
            tf['public'] = (_('Public'), lambda x: Q(public=x), [(True, _('Yes')), (False, _('No'))])
            tf['language'] = (_('Language'), lambda x: Q(language=x), list(LANG_CHOICE))
        return tf
