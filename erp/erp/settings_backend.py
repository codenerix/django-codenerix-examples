# -*- coding: utf-8 -*-
from erp.settings_base import *

ROOT_URLCONF = "erp.urls_backend"

ALLOWED_HOSTS += [
    "demoerp.codenerix.com",
    "www.demoerp.codenerix.com",
    # "erp.codenerix.com",
    # "www.erp.codenerix.com",
]


# URL for login
LOGIN_URL = "login"
# After doing login, where to go
LOGIN_REDIRECT_URL = "home"

# SSL Support forced
HTTPS_PATHS = ("/zzzzzzz",)
HTTPS_SUPPORT = False

ASGI_APPLICATION = "erp.asgi_backend.application"

# Spaguetti config
try:
    SPAGHETTIBOOL = SPAGHETTI
except Exception:
    SPAGHETTIBOOL = False
if DEBUG and SPAGHETTIBOOL:
    # List of apps
    SPAGHETTI_APPS = []
    for app in INSTALLED_APPS:
        if app.startswith("erp.") or app.startswith("codenerix"):
            SPAGHETTI_APPS.append(app)

    # Base config
    SPAGHETTI_SAUCE = {
        "apps": SPAGHETTI_APPS,
        "show_fields": False,
        "exclude": {"auth": ["user"]},
    }
