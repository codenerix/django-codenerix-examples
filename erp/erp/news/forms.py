from codenerix.forms import GenModelForm
from erp.news.models import News


class NewsForm(GenModelForm):
    class Meta:
        model = News
        exclude = []
