from django.db import models
from django.utils.translation import gettext_lazy as _

from codenerix.models import CodenerixModel


class Info(CodenerixModel):
    info = models.CharField(verbose_name=_("Info"), max_length=128)

    def __fields__(self, info):
        return (("info", _("Info")),)

    def __searchQ__(self, info, text):
        return {
            "contains_info": models.Q(info__icontains=text),
        }

    def __str__(self):
        return self.info

    def __unicode__(self):
        return self.__str__()
