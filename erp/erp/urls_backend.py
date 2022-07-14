from django.conf.urls import include
from django.urls import re_path as url
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
)
from django.conf.urls.static import static
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.conf import settings

# from erp.frontend.views import SlugLevelGet
from erp.frontend.views import OrderList  # , OrderDetails
from erp.frontend.views import InvoiceList  # , InvoiceDetails
from erp.frontend.views import WishListList  # , WishListDetails, WishListUpdate
from erp.frontend.views import (
    WishListProductList,
)  # , WishListProductCreate, WishListProductBuy, WishListProductDelete
from erp.frontend.views import BudgetList  # , BudgetDetails, BudgetUpdate
from erp.frontend.views import (
    ShoppingCart,
    Checkout,
    SearchProduct,
    ConfirmPayment,
)  # , CheckoutPayment

# from erp.frontend.views import frontend, not_authorized as frontend_not_authorized
from erp.base.views import alarms
from erp.base.views import not_authorized

urlpatterns = [
    # Site control
    url(
        r"^$",
        RedirectView.as_view(url=reverse_lazy("news_list"), permanent=True),
        name="home",
    ),
    url(r"^gest$", RedirectView.as_view(url=reverse_lazy("news_list"), permanent=True)),
    url(r"^codenerix/", include("codenerix.urls")),
    # url(r'^vendings/', include('erp.vendings.urls')),
    url(r"^vendings/", include("codenerix_vending.urls")),
    # url(r'^accounting/', include('erp.accounting.urls')),
    url(r"^codenerix_pos/", include("codenerix_pos.urls")),
    url(r"^common/", include("erp.common.urls")),
    url(r"^transports/", include("erp.transports.urls")),
    # Site places
    url(r"^people/", include("erp.people.urls")),
    url(r"^codenerix_products/", include("codenerix_products.urls")),
    url(r"^{}/".format(settings.CDNX_PRODUCTS_URL), include("codenerix_products.urls")),
    url(r"^codenerix_invoicing/", include("codenerix_invoicing.urls")),
    url(
        r"^{}/".format(settings.CDNX_INVOICING_URL_COMMON),
        include("codenerix_invoicing.urls"),
    ),
    url(
        r"^{}/".format(settings.CDNX_INVOICING_URL_PURCHASES),
        include("codenerix_invoicing.urls_purchases"),
    ),
    url(
        r"^{}/".format(settings.CDNX_INVOICING_URL_SALES),
        include("codenerix_invoicing.urls_sales"),
    ),
    url(r"^codenerix_storages/", include("codenerix_storages.urls")),
    url(
        r"^{}/".format(settings.CDNX_STORAGES_URL_COMMON),
        include("codenerix_storages.urls"),
    ),
    url(
        r"^{}/".format(settings.CDNX_STORAGES_URL_STOCKCONTROL),
        include("codenerix_storages.urls_stockcontrol"),
    ),
    url(r"^codenerix_reviews/", include("codenerix_reviews.urls")),
    url(r"^{}/".format(settings.CDNX_REVIEWS), include("codenerix_reviews.urls")),
    url(r"^codenerix_payments/", include("codenerix_payments.urls")),
    url(r"^{}/".format(settings.CDNX_PAYMENTS), include("codenerix_payments.urls")),
    url(r"^codenerix_geodata/", include("codenerix_geodata.urls")),
    url(r"^{}/".format(settings.CDNX_GEODATA_URL), include("codenerix_geodata.urls")),
    url(r"^codenerix_cms/", include("codenerix_cms.urls")),
    url(r"^codenerix_email/", include("codenerix_email.urls")),
    url(r"^news/", include("erp.news.urls")),
    url(r"^news/", include("erp.news.urls")),
    # url(r'^services/', include('erp.services.urls')),
    # url(r'^vendings/', include('erp.vendings.urls')),
    # url(r'^accounting/', include('erp.accounting.urls')),
    url(r"^codenerix_corporate/", include("codenerix_corporate.urls")),
    url(r"^i18n/", include("django.conf.urls.i18n")),
    url(r"^not_authorized/$", not_authorized, name="not_authorized"),
    # compatibilidad con frontend
    url(r"^backend/cart$", ShoppingCart.as_view(), name="shopping_cart"),
    url(r"^backend/budgets$", BudgetList.as_view(), name="shopping_cart_list"),
    url(r"^backend/invoices$", InvoiceList.as_view(), name="invoices_list"),
    url(r"^backend/orders$", OrderList.as_view(), name="orders_list"),
    url(r"^backend/wishlists$", WishListList.as_view(), name="wishlist_list"),
    url(
        r"^backend/wishlists$",
        WishListProductList.as_view(),
        name="wishlistproduct_list",
    ),
]

# Autoload
try:
    from erp.config import autourl

    urlpatterns = autourl(urlpatterns)
except Exception:
    print("Couldn't import autourl function in local configuration!")
    print("========================================================")
    raise

urlpatterns += [
    url(
        r"^confirmpayment/(?P<action>\w+)/(?P<error>\w+)/(?P<locator>\w+)$",
        ConfirmPayment.as_view(),
        name="confirm_payment",
    ),
    url(r"^backend/checkout$", Checkout.as_view(), name="checkout"),
    url(r"^buscar/$", SearchProduct.as_view(), name="buscar"),
    url(r"^search/$", SearchProduct.as_view(), name="search"),
    # User control
    url(r"^login/$", LoginView.as_view(), name="login"),
    url(r"^logout/$", LogoutView.as_view(), {"next_page": "/"}, name="logout"),
    url(r"^auth/", include("social_django.urls", namespace="social")),
    #  url(r'^singup$', CustomerRegister_people.as_view(), name='customer_singup'),  # <- NO DEBERIAN PODER INSCRIBIRSE
    url(r"^password/change/$", PasswordChangeView.as_view(), name="password_change"),
    url(
        r"^password/change/done/$",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    url(r"^password/reset/$", PasswordResetView.as_view(), name="password_reset"),
    url(
        r"^password/reset/done/$",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    url(
        r"^password/reset/complete/$",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    url(
        r"^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    # puesto aqui provisionamente
    url(r"^alarmspopups$", alarms, name="alarms"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
