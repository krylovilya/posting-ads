from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models


class CustomFlatPageAdmin(FlatPageAdmin):
    """Добавление wysiwyg редактора из ckeditor к простым страницам."""

    def __init__(self, *args):
        super().__init__(*args)
        self.formfield_overrides.update({
            models.TextField: {'widget': CKEditorWidget},
        })


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)
