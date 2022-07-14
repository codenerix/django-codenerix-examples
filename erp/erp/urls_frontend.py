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
from django.conf import settings

from codenerix_payments import urls as urlCodenerixPayment

from erp.frontend.views import (
    SlugLevelGet,
    BackendUser,
    OrderList,
    OrderDetails,
    InvoiceList,
    InvoiceDetails,
    WishListList,
    WishListDetails,
    WishListUpdate,
    WishListProductList,
    WishListProductCreate,
    WishListProductBuy,
    WishListProductDelete,
    BudgetList,
    BudgetDetails,
    BudgetUpdate,
    ShoppingCart,
    Checkout,
    SearchProduct,
    ConfirmPayment,
    CheckoutPayment,
    ListProductsFrontend,
    LineOrderSubList,
    RequestInvoice,
)

from erp.people.views import CustomerRegister
from erp.frontend.views import not_authorized as frontend_not_authorized
from erp.base.views import alarms

from erp.people.views import CustomerRegister as CustomerRegister_people
from erp.common.views import PublicContactFrontend

# Frontend
urlpatterns = [
    url(r"^not_authorized/$", frontend_not_authorized, name="not_authorized"),
    # url(r'^$', RedirectView.as_view(url=reverse_lazy('frontend',kwargs={'filename': 'index.html'}), permanent=True), name='home'),
    # url(r'^$', RedirectView.as_view(url=reverse_lazy('sluglevel1_get', kwargs={'slug1': 'index'}), permanent=True), name='home'),
    url(r"^$", SlugLevelGet.as_view(), kwargs={"slug1": "index"}, name="home"),
    # url(r'^test/(?P<slug1>[\w-]+)$', SlugLevelGet.as_view(), name='sluglevel1_get'),
    # url(r'^o/(?P<filename>[a-zA-Z0-9\.+/]+)$', frontend, name='frontend'),
    url(
        r"^request_invoice/(?P<orderk>\w+)$$",
        RequestInvoice.as_view(),
        name="request_invoice",
    ),
    url(r"^backend/$", BackendUser.as_view(), name="backend_user"),
    url(r"^backend/cart$", ShoppingCart.as_view(), name="shopping_cart"),
    url(
        r"^backend/checkoutpay/(?P<payment_method>\w+)$",
        CheckoutPayment.as_view(),
        name="checkout_pay",
    ),
    url(r"^backend/budgets$", BudgetList.as_view(), name="shopping_cart_list"),
    url(
        r"^backend/budgets/(?P<pk>\w+)$",
        BudgetDetails.as_view(),
        name="shopping_cart_details",
    ),
    url(
        r"^backend/budgets/(?P<pk>\w+)/edit$",
        BudgetUpdate.as_view(),
        name="shopping_cart_edit",
    ),
    url(r"^backend/wishlists$", WishListList.as_view(), name="wishlist_list"),
    url(
        r"^backend/wishlists/(?P<pk>\w+)$",
        WishListDetails.as_view(),
        name="wishlist_details",
    ),
    url(
        r"^backend/wishlists/(?P<pk>\w+)/edit$",
        WishListUpdate.as_view(),
        name="wishlist_edit",
    ),
    url(
        r"^backend/wishlistproducts$",
        WishListProductList.as_view(),
        name="wishlistproduct_list",
    ),
    url(
        r"^backend/wishlistproducts/add$",
        WishListProductCreate.as_view(),
        name="wishlistproduct_add",
    ),
    url(
        r"^backend/wishlistproducts/buy$",
        WishListProductBuy.as_view(),
        name="wishlistproduct_buy",
    ),
    url(
        r"^backend/wishlistproducts/(?P<pk>\w+)/delete$",
        WishListProductDelete.as_view(),
        name="wishlistproduct_delete",
    ),
    url(r"^backend/orders$", OrderList.as_view(), name="orders_list"),
    url(r"^backend/orders/(?P<pk>\w+)$", OrderDetails.as_view(), name="orders_details"),
    url(
        r"^backend/lineorders/(?P<pk>\w+)/sublist$",
        LineOrderSubList.as_view(),
        name="front_lineordersaless_sublist",
    ),
    url(r"^backend/invoices$", InvoiceList.as_view(), name="invoices_list"),
    url(
        r"^backend/invoices/(?P<pk>\w+)$",
        InvoiceDetails.as_view(),
        name="invoices_details",
    ),
    # ListProductsFrontend
    url(
        r"^listproducts/(?P<type>\w+)/(?P<pk>[0-9]+)$",
        ListProductsFrontend.as_view(),
        name="list_products_frontend",
    ),
    # url(r'^invoices/$', InvoicesUser.as_view(), name='invoices'),
    # url(r'^invoices_api/$', InvoicesUserAPI.as_view(), name='invoices_api'),
    # url(r'^wishlist/$', WishListUser.as_view(), name='wishlist'),
    # url(r'^wishlist_api/$', WishListUserAPI.as_view(), name='wishlist_api'),
    # url(r'^codenerix_products/', include('codenerix_products.urls')),
    url(r"^{}/".format(settings.CDNX_PRODUCTS_URL), include("codenerix_products.urls")),
    url(r"^{}/".format(settings.CDNX_GEODATA_URL), include("codenerix_geodata.urls")),
    url(
        r"^{}/".format(settings.CDNX_INVOICING_URL_SALES),
        include("codenerix_invoicing.urls_sales"),
    ),
    # url(r'^{}/'.format(settings.CDNX_REVIEWS), include('codenerix_reviews.urls')),
    url(r"^people/", include("erp.people.urls")),
    url(r"^contacto/", PublicContactFrontend.as_view(), name="form_contact"),
    url(r"^common/", include("erp.common.urls")),
    url(r"^transports/", include("erp.transports.urls")),
    # url(r'^profiles$', Profile.as_view(), name='profile_list'),
    # url(r'^profiles/(?P<pk>\w+)$', ProfileDetails.as_view(), name='profile_details'),
    # url(r'^profiles/(?P<pk>\w+)/edit$', ProfileUpdate.as_view(), name='profile_edit'),
    url(r"^codenerix/", include("codenerix.urls")),
    url(r"^codenerix_payments/", include("codenerix_payments.urls")),
    url(r"^{}/".format(settings.CDNX_PAYMENTS), include("codenerix_payments.urls")),
    url(r"^payments/", include(urlCodenerixPayment)),
    url(
        r"^confirmpayment/(?P<action>\w+)/(?P<error>\w+)/(?P<locator>\w+)$",
        ConfirmPayment.as_view(),
        name="confirm_payment",
    ),
    url(r"^backend/checkout$", Checkout.as_view(), name="checkout"),
    url(r"^buscar/$", SearchProduct.as_view(), name="buscar"),
    url(r"^search/$", SearchProduct.as_view(), name="search"),
    # User control
    url(r"^login/$", CustomerRegister.as_view(), name="login"),
    url(r"^logout/$", LogoutView.as_view(), {"next_page": "/"}, name="logout"),
    url(r"^auth/", include("social_django.urls", namespace="social")),
    url(r"^singup$", CustomerRegister_people.as_view(), name="customer_singup"),
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
    #     ^(?P<slug1>\w+(\-*\w+|)*)/(?P<slug2>\w+(\-*\w+|)*)$
    #     ^(\w+(\-*\w+|)*)/(\w+(\-*\w+|)*)$
    # url(r'^(?P<slug1>\w+(\-*\w+|)*)/(?P<slug2>\w+(\-*\w+|)*)$', SlugLevelGet.as_view(), name='sluglevel2_get'),
    # url(r'^(?P<slug1>\w+(\-*\w+|)*)/(?P<slug2>\w+(\-*\w+|)*)$', SlugLevelGet.as_view(), name='sluglevel2_get'),
    url(
        r"^(?P<slug1>[-\w\d]+)/(?P<slug2>[-\w\d]+)/(?P<slug3>[-\w\d]+)$",
        SlugLevelGet.as_view(),
        name="sluglevel3_get",
    ),
    url(
        r"^(?P<slug1>[-\w\d]+)/(?P<slug2>[-\w\d]+)$",
        SlugLevelGet.as_view(),
        name="sluglevel2_get",
    ),
    url(r"^(?P<slug1>\w+(-*\w+|)*)$", SlugLevelGet.as_view(), name="sluglevel_get"),
    url(r"^(?P<slug1>[\w-]+)$", SlugLevelGet.as_view(), name="sluglevel1_get"),
    # url(r"^rosetta/", include("rosetta.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
