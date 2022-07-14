from django.urls import re_path as url

from erp.news.views import NewsList, NewsCreate, NewsUpdate, NewsDelete

# Querysets
#info_news = { 'queryset': News.objects.filter( \
#                          (Q(web_from__isnull=True)  | Q(web_from__lte=datetime.datetime.now())) \
#                        & (Q(web_until__isnull=True) | Q(web_until__gte=datetime.datetime.now()))), \
#                        'permission':'news.view_news'}
#info_news_admin = { 'queryset': News.objects.all(), 'permission':'news.view_news', 'permission_group':'Admins' }

# URLs
urlpatterns = [
    url(r'^newss$', NewsList.as_view(), name='news_list'),
    url(r'^newss/add$', NewsCreate.as_view(), name='news_add'),
    url(r'^newss/(?P<pk>\w+)/edit$', NewsUpdate.as_view(), name='news_edit'),
    url(r'^newss/(?P<pk>\w+)/delete$', NewsDelete.as_view(), name='news_delete'),
]
