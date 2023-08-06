from django.db import models
from django.utils.html import format_html

from .choices import StyleChoices


class FontIconModel(models.Model):
    style = models.CharField(max_length=6, choices=StyleChoices.choices, default=StyleChoices.fas)
    icon_name = models.CharField(max_length=200, default='')
    active = models.BooleanField(default=True)

    def __str__(self):
        return '<i class="{0} {1}"></i> {2}'.format(self.style, self.icon_name, self.stripped_name())

    def stripped_name(self):
        return self.icon_name[3:]

    def to_html(self):
        return format_html('<i class="{0} {1}"></i>'.format(self.style, self.icon_name))


class IconForeignKeyField(models.ForeignKey):

    description = "A hand of cards (bridge style)"

    def __init__(self, **kwargs):
        kwargs['to'] = 'font_icons.FontIconModel'
        kwargs['on_delete'] = models.SET_NULL
        super().__init__(**kwargs)

    def formfield(self, *, using=None, **kwargs):
        from .fields import IconChoiceField

        return super().formfield(**{
            'form_class': IconChoiceField,
            'queryset': self.remote_field.model._default_manager.using(using),
            'to_field_name': self.remote_field.field_name,
            **kwargs,
        })
