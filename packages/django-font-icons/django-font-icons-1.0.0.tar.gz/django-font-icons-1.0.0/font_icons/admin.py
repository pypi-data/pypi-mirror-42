from django.contrib import admin
from django.utils.html import format_html

from .models import FontIconModel


def make_active(modeladmin, request, queryset):
    queryset.update(active=True)


def make_inactive(modeladmin, request, queryset):
    queryset.update(active=False)


@admin.register(FontIconModel)
class FontIconModelAdmin(admin.ModelAdmin):
    list_display = ('show', 'icon_name', 'style', 'active')
    list_filter = ('style', 'active')
    search_fields = ('icon_name', )

    actions = [make_active, make_inactive]

    def show(self, obj):
        return format_html('<i class="{} {}"></i>'.format(obj.style, obj.icon_name))
