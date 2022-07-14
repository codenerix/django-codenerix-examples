from django.contrib import admin
from erp.news.models import News


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'created', 'updated', 'web_from', 'web_until', 'public', 'language')
    list_filter = ['public', 'language']
    search_fields = ['title', 'subtitle', 'content']
    date_hierarchy = 'updated'


admin.site.register(News, NewsAdmin)
