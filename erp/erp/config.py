DEBUG = True
DEBUG_PQPRO = True
ROSETTA = True
# ROSETTA = False
ADMINSITE = True
DEBUG_TOOLBAR = False
DEBUG_PANEL = False
SPAGHETTI = False
MEMCACHE = False
SNIPPET_SCREAM = False
# APPEND_SLASH = True
ADMINS = (("Nobody", "nobody@domain.dom"),)
CLIENTS = ADMINS
HTTPS_SUPPORT = False

# Email server
EMAIL_HOST = "127.0.0.1"
EMAIL_HOST_USER = "test@localhost"
AIL_HOST_PASSWORD = "asdfasdfasdf"
DEFAULT_FROM_EMAIL = "erp@localhost"

EMAIL_FROM = "erp.xxx@localhost"
EMAIL_HOST = "localhost"
EMAIL_PORT = 465
EMAIL_USERNAME = "erp.xxx@localhost"
EMAIL_PASSWORD = "asdfasdfasdf"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

# EMAIL_FROM = "codenerixerpcloud@gmail.com"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 465
# EMAIL_USERNAME = "codenerixerpcloud@gmail.com"
# EMAIL_PASSWORD = "asdfasdfasdfasdf"
# EMAIL_USE_TLS = False
# EMAIL_USE_SSL = True
# EMAIL_BACKEND = "codenerix.lib.genmail.SSLEmailBackend"

CLIENT_EMAIL_FROM = EMAIL_FROM
CLIENT_EMAIL_HOST = EMAIL_HOST
CLIENT_EMAIL_PORT = EMAIL_PORT
CLIENT_EMAIL_USERNAME = EMAIL_USERNAME
CLIENT_EMAIL_PASSWORD = EMAIL_PASSWORD
CLIENT_EMAIL_USE_TLS = EMAIL_USE_TLS
CLIENT_EMAIL_USE_SSL = EMAIL_USE_SSL

# SECRET KEY
SECRET_KEY = "asdfa-CODENERIX-CODENERIX-CODENERIX-asdfasdfff2"

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = (
    "asdfasdfasdfasdfa.apps.googleusercontent.com"  # Paste CLient Key
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "asdfasdfasdf"  # Paste Secret Key

# DATABASES
# DATABASE_APPS_MAPPING = {'mysql': 'mysql', 'default':'default'}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",  # Engine (Supported: 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle')
        "NAME": "erp",  # Database name
        "USER": "erp",  # Username
        "PASSWORD": "asdfasdfasdfasdf",  # Password
        "HOST": "",  # Host (empty=localhost)
        "PORT": "",  # Port (empty=3306)
        "OPTIONS": {
            # "init_command": "SET storage_engine=INNODB; SET time_zone='UTC'; SET sql_mode='STRICT_TRANS_TABLES';"
        },
    },
}

# MEMCACHE
if MEMCACHE:
    CACHE_BACKEND = "memcached://127.0.0.1:11211/"
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
            "LOCATION": "127.0.0.1:11211",
            "KEY_PREFIX": "I",
            "TIMEOUT": 1800,
        },
        "debug-panel": {
            "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
            "LOCATION": "/tmp/debug-panel-cache",
            "TIMEOUT": 300,
            "OPTIONS": {"MAX_ENTRIES": 500},
        },
    }


# autoload = lambda a,b: return (a,b)
# autourl = lambda a: return a

BASE_URL = ""
# Configuration for DEBUGGERS
from codenerix.debug import (
    codenerix_statics,
    DEBUG_TOOLBAR_DEFAULT_PANELS,
    DEBUG_TOOLBAR_DEFAULT_CONFIG,
    autoload as autoload_debug,
    autourl as autourl_debug,
)

(CODENERIX_CSS, CODENERIX_JS) = codenerix_statics(DEBUG)

if DEBUG and DEBUG_TOOLBAR:
    INTERNAL_IPS = ("127.0.0.1",)  # Use: ('',) for everybody
    DEBUG_TOOLBAR_PANELS = DEBUG_TOOLBAR_DEFAULT_PANELS
    DEBUG_TOOLBAR_CONFIG = DEBUG_TOOLBAR_DEFAULT_CONFIG

if DEBUG and ROSETTA:
    ADMIN_MEDIA_PREFIX = "/static/admin/"
    # ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS=True
    # ROSETTA_GOOGLE_TRANSLATE=True

AUTHENTICATION_TOKEN = {
    #              'key': 'hola',
    #  'master_unsigned': True,
    #    'master_signed': True,
    #    'user_unsigned': True,
    #      'user_signed': True,
    #     'otp_unsigned': True,
    #       'otp_signed': True,
}

if DEBUG and SPAGHETTI:
    SPAGHETTI_APPS = []
    # SPAGHETTI_APPS.append('codenerix')
    SPAGHETTI_APPS.append("base")
    SPAGHETTI_APPS.append("sales")
    SPAGHETTI_APPS.append("purchases")
    SPAGHETTI_APPS.append("people")
    SPAGHETTI_APPS.append("codenerix_products")
    # SPAGHETTI_APPS.append('storages')
    # SPAGHETTI_APPS.append('alarms')
    SPAGHETTI_SAUCE = {
        "apps": SPAGHETTI_APPS,
        "show_fields": False,
        "exclude": {"auth": ["user"]},
    }

# Autoload for DEBUG system
# autoload = lambda INSTALLED_APPS, MIDDLEWARE_CLASSES: autoload_debug(INSTALLED_APPS, MIDDLEWARE_CLASSES, DEBUG, SPAGHETTI, ROSETTA, ADMINSITE, DEBUG_TOOLBAR, DEBUG_PANEL, SNIPPET_SCREAM, None)
autoload = lambda INSTALLED_APPS, MIDDLEWARE_CLASSES: autoload_debug(
    INSTALLED_APPS,
    MIDDLEWARE_CLASSES,
    DEBUG,
    SPAGHETTI,
    ROSETTA,
    ADMINSITE,
    DEBUG_TOOLBAR,
    DEBUG_PANEL,
    SNIPPET_SCREAM,
    None,
)
autourl = lambda URLPATTERNS: autourl_debug(
    URLPATTERNS, DEBUG, ROSETTA, ADMINSITE, SPAGHETTI
)

from django.utils.translation import gettext as _

PAYMENTS = {
    "meta": {
        "name": "Codenerix",
        "url": "http://localhost:81",
        "urlssl": "https://localhost:444",
        "real": False,
        "taxes": 21,
        "redirects_default": "https://localhost/algunlado/",
        "redirects": {},
    },
    "paypal": {
        "name": "Paypal",
        "protocol": "paypal",
        "id": "123412341234",
        "secret": "MTIzNDEzMjM0MTIzNAo=",
    },
    "redsys": {
        "name": "Redsys",
        "protocol": "redsys",
        # REAL
        # 'endpoint': 'https://sis.redsys.es/sis/realizarPago',
        # 'merchant_code': '123456789',
        # 'auth_key': 'asdfasdfasdfasdfasfdasdfasdfasdf',
        #  --- --- --- --- --- ---
        #  SANDBOX
        "endpoint": "https://sis-t.redsys.es:25443/sis/realizarPago",
        # 'endpoint': 'https://sis-t.redsys.es:25443/sis/services/SerClsWSEntrada', # XML
        "merchant_code": "123456789",
        "auth_key": "asdfasfdasdfasdfasdfasdfasdfasdf",
    },
    "yeepay": {
        "name": "Yeepay",
        "protocol": "yeepay",
        "endpoint": "https://cashdesk.yeepay.com",
        "customerNo": 123412341234,
        "customerId": "irt_123412341234",
        "private_key": "MIICXgIBAAKBgQCCMfXBc/TFqOpI5enjcAfWtrko/EK5g9hJmyDApyQiQrjIZEY+tOYRQk1BfVvy3ZY6N+YC+JNrxw19GbHemthNjtjv3jUkguBCY55d+YAsnEi0rJmC14DO0lo17Z6jAWsIQbke5BIwn0bRA/samYRSLgzVK7wU7OHLru4jqtiNWwIDAQABAoGAcRWr/GgXh0f8l2z8BkzcwibcFTlnS3O1fdl8TVngDNIfZg+S5AyEeSE5sVSNdRn6zn6XDqWSht7SXILg+BVPImXcrTjAz2v809dGHKWaHdjE1I+FloBwZjZqx0umUKNgLr6NMYSHReF8JsrHV9Bb+MdEW6FPeUrt8enJXjgnj8ECQQDvE861vgBE+CDUJKhR68fKAZu4NQUSA4oztNoDiRujwLu4+uvs+nSuQ5FA+6QGKAGQQemM/ewQgL/nJ+BdXMMDAkEAi2koCpg9h9cK26ZN7pHFGl182G2aQbnAtmMGud3aEjvtc1YiDEMYM/6ESUaB9sSp06V0WKBJTVEao/GdudvQyQJBAJeyicbn+GPKzYnOeL8CTJLw0k3f1ofHlzmX133G0bLl6DdHf8uuX7rzRIdnJHyDhfpy2C6OL+uIxjt2IfcblOECQQCEXhoIxThXDFVg7Oy+AmZVfEKX9KksksRp6GhwfjcabRAuHLBDWElYxOax9GJd/akKLeTkaXxwDvvugfEykYYRAkEAwoboYL/G6c04w+ntSEsF5GakEJ7onYOr2sxyrxehdkgwoZ2CYoEEp03vtxUa2qzNAnHq8MI0HCJVMI6RhxAU0A==",
        "public_key": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCCMfXBc/TFqOpI5enjcAfWtrko/EK5g9hJmyDApyQiQrjIZEY+tOYRQk1BfVvy3ZY6N+YC+JNrxw19GbHemthNjtjv3jUkguBCY55d+YAsnEi0rJmC14DO0lo17Z6jAWsIQbke5BIwn0bRA/samYRSLgzVK7wU7OHLru4jqtiNWwIDAQAB",
    },
}


# WS4REDIS_CONNECTION = {
#     'host': '127.0.0.1',
#     'port': 6379,
#     'db': 1,
#     'password': 'asdfasdfasdfasdffasdfasdfasd',
# }
# WEBSOCKET_URL = '/ws/'
WEBSOCKET_URL = "127.0.0.1"
WEBSOCKET_PORT = 8000

# Channels settings
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",  # use redis backend
        "CONFIG": {
            # "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],  # set redis address
            "hosts": [("redis://:asdfasdf@localhost:6379/0")],  # set redis address
        },
    },
}
# Celery settings
# BROKER_URL = 'redis://localhost:6379/0'  # our redis address
# use json format for everything
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_USER = 'erp'
# CELERY_PASSWORD = 'asdfasdfasdf'
# BROKER_URL = 'amqp://username:password@jobs.yoursite.com:5762//'


def gettext(s):
    return s


TRANSPORTS = {
    "meta": {
        "real": False,
    },
    "domicilio": {
        "name": gettext("A Domicilio"),
        "protocol": "dummy",
        "logic": [
            (50, 8.9),
            (None, 0),
        ],
        "price_base": 0,
        "description": gettext(
            "A Domicilio (Gasto de envio gratuito para pedidos superiores a 50 euros, siempre y cuando el envio se realice dentro de la peninsula. No se realizan envios a canarias)  Para envios a Europa el coste sera de 8,90 euros"
        ),
    },
}
