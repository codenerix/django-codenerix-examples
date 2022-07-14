from django.contrib import admin

from .models import Person, Company, PersonAddress
from .models import Publicist, Authorship


class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname')
    # Will add a filtering column on the right to make easy to look for registers
    list_filter = []
    # Will add a search box for questions on the top
    search_fields = ['user', 'name', 'surname']
    # New row for filtering dates by groups of years, months, days in one click (hierarchycal navigation)
    # date_hierarchy = 'user.date_joined'


admin.site.register(Person, PersonAdmin)
admin.site.register(PersonAddress)
admin.site.register(Company)
admin.site.register(Publicist)
admin.site.register(Authorship)
