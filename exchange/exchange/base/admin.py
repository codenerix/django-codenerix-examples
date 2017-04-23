from django.contrib import admin

from .models import Currency, Exchange


admin.site.register(Currency)
admin.site.register(Exchange)
