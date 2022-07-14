from codenerix.views import GenList, GenCreate, GenUpdate, GenDelete

from erp.news.models import News
from erp.news.forms import NewsForm


class NewsList(GenList):
    model = News


class NewsCreate(GenCreate):
    model = News
    form_class = NewsForm


class NewsUpdate(GenUpdate):
    model = News
    form_class = NewsForm


class NewsDelete(GenDelete):
    model = News
