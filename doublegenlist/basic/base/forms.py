from codenerix.forms import GenModelForm
from basic.base.models import Info


class InfoForm(GenModelForm):
    class Meta:
        model = Info
        fields = ("info",)

    def __groups__(self):
        return [
            (
                None,
                12,
                ["info", 12],
            )
        ]
