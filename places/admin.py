from django.contrib import admin
from django.utils.html import format_html
from places.models import Place, Image

from adminsortable2.admin import SortableStackedInline, SortableAdminBase


class ImageStackedInline(SortableStackedInline):
    model = Image
    extra = 1
    readonly_fields = ['img_preview']

    def img_preview(self, obj):
        return format_html(
            '<img src="{}" width="{}" height="{}" />',
            obj.image.url, 'auto', 200
        )

    img_preview.short_description = 'превью'

    fields = ('image', 'img_preview', 'order')


@admin.register(Image)
class SortableImageAdmin(SortableAdminBase, admin.ModelAdmin):
    pass


@admin.register(Place)
class SortablePlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageStackedInline]