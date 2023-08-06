from django import forms
from django.db import models
from django.utils.html import format_html

from .models import FontIconModel
from .widget import IconSelect


class IconChoiceField(forms.ModelChoiceField):
    to_field_name = None
    widget = IconSelect

    def __init__(self, *args, **kwargs):
        kwargs['queryset'] = FontIconModel.objects.filter(active=True)
        super().__init__(**kwargs)

    def _get_queryset(self):
        return self._queryset.filter(active=True)

    def label_from_instance(self, obj):
        return '<i class="{} {}"></i> {}'.format(obj.style, obj.icon_name, obj.stripped_name())
