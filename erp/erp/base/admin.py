from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name=str(value)
            output.append(u' <a href="%s" target="_blank"><img src="%s" alt="%s" /></a> %s ' % (image_url, image_url, file_name, "%s:" % (_('Change'))))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

class MyAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ['logo','picture']:
            request = kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(MyAdmin,self).formfield_for_dbfield(db_field, **kwargs)

