# -*- coding: utf-8 -*-
from erp.settings_base import *

ROOT_URLCONF = "erp.urls_frontend"

ALLOWED_HOSTS += [
    "demo.codenerix.com",
    "www.demo.codenerix.com",
    # "codenerix.com",
    # "www.codenerix.com",
]


# URL for login
LOGIN_URL = "login"
# After doing login, where to go
LOGIN_REDIRECT_URL = "home"

ASGI_APPLICATION = "erp.asgi_frontend.application"
