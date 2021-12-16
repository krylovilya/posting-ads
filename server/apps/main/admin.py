from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models

from ckeditor.widgets import CKEditorWidget

from apps.main.models import Ad, Category, Picture, Seller, SMSLog, Subscription, Tag


class CustomFlatPageAdmin(FlatPageAdmin):
    """Добавление wysiwyg редактора из ckeditor к простым страницам."""

    def __init__(self, *args):
        super().__init__(*args)
        self.formfield_overrides.update({
            models.TextField: {'widget': CKEditorWidget},
        })


class CustomSellerAdmin(admin.ModelAdmin):
    """Добавление свойства num_ads в админку."""

    list_display = ('__str__', 'num_ads')


@admin.action(description='Архивировать выбранные объявления')
def archive(modeladmin, request, queryset):
    queryset.update(archive=True)


class CustomAdAdmin(admin.ModelAdmin):
    """Добавление фильтрации и архивирование объявлений."""
    list_filter = ('tags', 'creation_date')
    actions = (archive,)


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)

admin.site.register(Ad, CustomAdAdmin)
admin.site.register(Category)
admin.site.register(Seller, CustomSellerAdmin)
admin.site.register(Picture)
admin.site.register(Tag)
admin.site.register(SMSLog)
admin.site.register(Subscription)
