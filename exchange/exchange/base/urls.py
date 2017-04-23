from django.conf.urls import url

from .views import CurrencyList, CurrencyCreate, CurrencyCreateModal, CurrencyUpdate, CurrencyUpdateModal, CurrencyDelete, CurrencyForeign, CurrencyOnline
from .views import ExchangeList, ExchangeCreate, ExchangeDetail, ExchangeUpdate, ExchangeDelete


urlpatterns = [
    # Contacts Routes
    url('^currencys$', CurrencyList.as_view(), name='currency_list'),
    url('^currencys/add$', CurrencyCreate.as_view(), name='currency_add'),
    url('^currencys/addmodal$', CurrencyCreateModal.as_view(), name='currency_addmodal'),
    url('^currencys/(?P<pk>\w+)/edit$', CurrencyUpdate.as_view(), name='currency_edit'),
    url('^currencys/(?P<pk>\w+)/editmodal$', CurrencyUpdateModal.as_view(), name='currency_editmodal'),
    url('^currencys/(?P<pk>\w+)/delete$', CurrencyDelete.as_view(), name='currency_delete'),
    url('^currencys/(?P<sell>\w+)/(?P<buy>\w+)/online$', CurrencyOnline.as_view(), name='currency_online'),
    url('^currencys/(?P<search>[\w\W]+|\*)$', CurrencyForeign.as_view(), name='currency_foreign'),

    # Exchanges Routes
    url('^exchanges$', ExchangeList.as_view(), name='exchange_list'),
    url('^exchanges/add$', ExchangeCreate.as_view(), name='exchange_add'),
    url('^exchanges/(?P<pk>\w+)$', ExchangeDetail.as_view(), name='exchange_detail'),
    url('^exchanges/(?P<pk>\w+)/edit$', ExchangeUpdate.as_view(), name='exchange_edit'),
    url('^exchanges/(?P<pk>\w+)/delete$', ExchangeDelete.as_view(), name='exchange_delete'),
]
