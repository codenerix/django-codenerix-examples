# -*- coding: utf-8 -*-
# Django settings for erp project.
import os

VERSION = "0.1"


DEBUG = True
DEBUG_AUTH = False
# DEBUG_PROPAGATE_EXCEPTIONS = True

# Behaviour
# APPEND_SLASH = True
# Behavior configuration
USERNAME_MIN_SIZE = 6
PASSWORD_MIN_SIZE = 8
ALARMS_LOOPTIME = 15000  # Refresh alarms every 15 seconds (15.000 miliseconds)
ALARMS_QUICKLOOP = 1000  # Refresh alarms every 1 seconds (1.000 miliseconds) when the system is on quick loop processing (without focus)
ALARMS_ERRORLOOP = 5000  # Refresh alarms every 5 seconds (5.000 miliseconds) when the http request fails
CONNECTION_ERROR = 60000  # Connection error after 60 seconds (60.000 miliseconds)
ALL_PAGESALLOWED = True
COLORS = {
    "people": {
        "pilot": "#BBDDFF",
        "cockpit": "#FFDDBB",
        "crew": "#FFFFBB",
        "passengers": "#DDFFBB",
    }
}

CODENERIX_CSS = '<link href="/static/codenerix/codenerix.css" rel="stylesheet">'
CODENERIX_JS = (
    '<script type="text/javascript" src="/static/codenerix/codenerix.js"></script>'
)
CODENERIX_JS += '<script type="text/javascript" src="/static/codenerix/codenerix.extra.js"></script>'


# Autoload
def autoload(*args):
    return args


def autourl(arg):
    return arg


ALLOWED_HOSTS = [
    # "codenerix.com",
    # "www.codenerix.com",
    "localhost",
    "127.0.0.1",
    # "erp.es",
    # "www.erp.es",
]


# Import configuration file
try:
    from erp.config import *
except Exception:
    print("Couldn't import local configuration!")
    print("====================================")
    raise

try:
    from erp.profiles import *
except Exception:
    print("Couldn't import profiles configuration!")
    print("====================================")
    raise

try:
    from erp.datas_project import *
except Exception:
    print("Couldn't import profiles configuration!")
    print("====================================")
    raise

# Define base dir
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
# TIME_ZONE = 'UTC'
TIME_ZONE = "Europe/Madrid"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = "es-es"


def ugettext(s):
    return s


LANGUAGES = (
    ("es", ugettext("Spanish")),
    # ('en', ugettext('English')),
    # ('pl', ugettext('Polish')),
)
LANGUAGES_DATABASES = ["ES", "EN"]


SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# Use this serializer to be able to serialize timezone dates
SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"

# Other definitions about dates, hours
# DATETIME_FORMAT = "Y-m-d H:i"
DATETIME_FORMAT = "d-m-Y H:i"
# DATETIME_INPUT_FORMATS = ("%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M:%S",)
DATETIME_INPUT_FORMATS = (
    "%d-%m-%Y %H:%M",
    "%d/%m/%Y %H:%M:%S",
)
DATETIME_DDBB_FORMATS = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "H:i"
TIME_INPUT_FORMATS = ("%H:%M", "%H%M", "%H:%M:%S")
DATETIME_RANGE_FORMAT = (
    "%Y-%m-%d",
    "YYYY-MM-DD",
    "%Y/%m/%d",
    "YYYY/MM/DD",
)  # ATENCION: el formato que llega a la funcion es mayor
# DATETIME_RANGE_FORMAT = ("%d-%m-%Y", "DD-MM-YYYY", "%d/%m/%Y", "DD/MM/YYYY") # ATENCION: el formato que llega a la funcion es mayor

DATERANGEPICKER_OPTIONS = "{{"
DATERANGEPICKER_OPTIONS += "    format: '{Format}',"
DATERANGEPICKER_OPTIONS += "    timePicker:true,"
DATERANGEPICKER_OPTIONS += "    timePicker12Hour:false,"
DATERANGEPICKER_OPTIONS += "    showDropdowns: true,"
DATERANGEPICKER_OPTIONS += "    locale: {{"
DATERANGEPICKER_OPTIONS += "        firstDay:1,"
DATERANGEPICKER_OPTIONS += "        fromLabel:'{From}',"
DATERANGEPICKER_OPTIONS += "        toLabel:'{To}',"
DATERANGEPICKER_OPTIONS += "        applyLabel:'{Apply}',"
DATERANGEPICKER_OPTIONS += "        cancelLabel:'{Cancel}',"
DATERANGEPICKER_OPTIONS += (
    "        daysOfWeek: ['{Su}', '{Mo}', '{Tu}', '{We}', '{Th}', '{Fr}','{Sa}'],"
)
DATERANGEPICKER_OPTIONS += "        monthNames: ['{January}', '{February}', '{March}', '{April}', '{May}', '{June}', '{July}', '{August}', '{September}', '{October}', '{November}', '{December}'],"
DATERANGEPICKER_OPTIONS += "    }},"
DATERANGEPICKER_OPTIONS += "}}"

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# LOCALE_PATHS
LOCALE_PATHS = (os.path.join(BASE_DIR, "conf/locale"),)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "erp/templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "codenerix.context.codenerix",
                "codenerix.context.codenerix_js",
                "erp.context.project_context",
                # 'django.core.context_processors.request',
            ],
        },
    },
]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "codenerix.authbackend.TokenAuthMiddleware",
    "codenerix.authbackend.LimitedAuthMiddleware",
    # 'codenerix_pos.authbackend.POSAuthMiddleware',
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "codenerix.middleware.SecureRequiredMiddleware",
    "codenerix.middleware.CurrentUserMiddleware",
]

WSGI_APPLICATION = "erp.wsgi.application"

# Python dotted path to the WSGI application used by Django's runserver.
# WSGI_APPLICATION = 'erp.wsgi.application'

AUTHENTICATION_BACKENDS = (
    # "django.contrib.auth.backends.ModelBackend",  # Django's default
    "codenerix.authbackend.TokenAuth",  # TokenAuth
    "codenerix.authbackend.LimitedAuth",  # LimitedAuth
    "codenerix_pos.authbackend.POSAuth",  # POSAuth
    "social_core.backends.google.GoogleOAuth2",  # for Google authentication
    "social_core.backends.github.GithubOAuth2",  # for Github authentication
    "social_core.backends.facebook.FacebookOAuth2",  # for Facebook authentication
)

AUTHENTICATION_TOKEN = {
    # 'key': 'hola',
    # 'master_unsigned': True,
    # 'master_signed': True,
    # 'user_unsigned': True,
    # 'user_signed': True,
    # 'otp_unsigned': True,
    # 'otp_signed': True,
}

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "erp.common",
    "channels",
    "social_django",
    "django_extensions",
    # Codenerix
    "codenerix",
    "codenerix_extensions",
    "codenerix_corporate",
    "codenerix_geodata",
    "codenerix_products",
    "codenerix_storages",
    "codenerix_pos",
    "codenerix_invoicing",
    "codenerix_payments",
    "codenerix_reviews",
    "codenerix_cms",
    "codenerix_email",
    "codenerix_transports",
    "codenerix_vending",
    # Project
    "erp.base",
    "erp.people",
    "erp.frontend",
    "erp.news",
    "erp.transports",
)

# Test runner
# TEST_RUNNER = 'django.test.runner.DiscoverRunner'
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}


# Autoload
(INSTALLED_APPS, MIDDLEWARE) = autoload(INSTALLED_APPS, MIDDLEWARE)

LIMIT_FOREIGNKEY = 25

# path for codenerix_invoicing
CDNX_INVOICING_URL_COMMON = "invoicing"
CDNX_INVOICING_URL_PURCHASES = "purchases"
CDNX_INVOICING_URL_SALES = "sales"

CDNX_INVOICING_LOGICAL_DELETION = True

CDNX_INVOICING_CODE_FORMAT_BUDGET = (
    "B{year}{day}{month}-{hour}{minute}-{serial}-{number}"
)
CDNX_INVOICING_CODE_FORMAT_WISHLIST = (
    "W{year}{day}{month}-{hour}{minute}-{serial}-{number}"
)
CDNX_INVOICING_CODE_FORMAT_SHOPPINGCART = (
    "S{year}{day}{month}-{hour}{minute}-{serial}-{number}"
)
CDNX_INVOICING_CODE_FORMAT_ORDER = (
    "O{year}{day}{month}-{hour}{minute}-{serial}-{number}"
)
CDNX_INVOICING_CODE_FORMAT_ALBARAN = (
    "A{year}{day}{month}-{hour}{minute}-{serial}-{number}"
)
CDNX_INVOICING_CODE_FORMAT_TICKET = (
    "T{year}{day}{month}-{hour}{minute}-{serial}-{number}"
)
CDNX_INVOICING_CODE_FORMAT_TICKETRECTIFICATION = (
    "TR{year}{day}{month}-{hour}{minute}-{serial}-{number}"
)
CDNX_INVOICING_CODE_FORMAT_INVOICE = (
    "I{year}{day}{month}-{hour}{minute}-{serial}-{number}"
)
CDNX_INVOICING_CODE_FORMAT_INVOICERECTIFCATION = (
    "IT{year}{day}{month}-{hour}{minute}-{serial}-{number}"
)

CDNX_INVOICING_CURRENCY_MAX_DIGITS = 10  # 99.999.999,?$
CDNX_INVOICING_CURRENCY_DECIMAL_PLACES = 2  # ?,99$

CDNX_INVOICING_FORCE_STOCK_IN_BUDGET = True
CDNX_INVOICING_FORCE_STOCK_IN_BUDGET = False

# path for codenerix_invoicing
CDNX_STORAGES_URL_COMMON = "storages"
CDNX_STORAGES_URL_STOCKCONTROL = "stockcontrol"
# path for codenerix_reviews
CDNX_REVIEWS = "reviews"
# path for codenerix_products
CDNX_PRODUCTS_URL = "products"
CDNX_PRODUCTS_SHOW_ONLY_STOCK = False
CDNX_PRODUCTS_NOVELTY_DAYS = 5
CDNX_PRODUCTS_FORCE_STOCK = False
# path for codenerix_payments
CDNX_PAYMENTS = "payments"
# path for codenerix_geodata
CDNX_GEODATA_URL = "geodata"
CASHDIARY_CLOSES_AT = "05:00"
CASHDIARY_ERROR_MARGIN = 0.5

# URL for Codenerix Payments
CDNX_PAYMENTS = "payments"
CDNX_PAYMENTS_REQUEST_CREATE = True
CDNX_PAYMENTS_REQUEST_UPDATE = True
CDNX_PAYMENTS_REQUEST_DELETE = True
CDNX_PAYMENTS_REQUEST_PAY = True

RECAPTCHA_PUBLIC_KEY = "6LeeLDkUAAAAAO9hiKxgR_0yo6_kAdkM7aLWAX2a"
RECAPTCHA_PRIVATE_KEY = "6LeeLDkUAAAAAMVQV2IvO-2eUOk-ax8WCbFv0PDo"

NOCAPTCHA = True
# RECAPTCHA_USE_SSL = True

INFO_TERMS_VENDING = "img/terms_ticket_vending.png"
