from django.urls import re_path

from .views import CurrencyList, CurrencyCreate, CurrencyCreateModal, CurrencyUpdate, CurrencyUpdateModal, CurrencyDelete, CurrencyForeign, CurrencyOnline
from .views import ExchangeList, ExchangeCreate, ExchangeDetail, ExchangeUpdate, ExchangeDelete


urlpatterns = [
    # Contacts Routes
    re_path('^currencys$', CurrencyList.as_view(), name='currency_list'),
    re_path('^currencys/add$', CurrencyCreate.as_view(), name='currency_add'),
    re_path('^currencys/addmodal$', CurrencyCreateModal.as_view(), name='currency_addmodal'),
    re_path('^currencys/(?P<pk>\w+)/edit$', CurrencyUpdate.as_view(), name='currency_edit'),
    re_path('^currencys/(?P<pk>\w+)/editmodal$', CurrencyUpdateModal.as_view(), name='currency_editmodal'),
    re_path('^currencys/(?P<pk>\w+)/delete$', CurrencyDelete.as_view(), name='currency_delete'),
    re_path('^currencys/(?P<sell>\w+)/(?P<buy>\w+)/online$', CurrencyOnline.as_view(), name='currency_online'),
    re_path('^currencys/(?P<search>[\w\W]+|\*)$', CurrencyForeign.as_view(), name='currency_foreign'),

    # Exchanges Routes
    re_path('^exchanges$', ExchangeList.as_view(), name='exchange_list'),
    re_path('^exchanges/add$', ExchangeCreate.as_view(), name='exchange_add'),
    re_path('^exchanges/(?P<pk>\w+)$', ExchangeDetail.as_view(), name='exchange_detail'),
    re_path('^exchanges/(?P<pk>\w+)/edit$', ExchangeUpdate.as_view(), name='exchange_edit'),
    re_path('^exchanges/(?P<pk>\w+)/delete$', ExchangeDelete.as_view(), name='exchange_delete'),
]
