from django import forms
from django.forms.widgets import Select


class IconSelect(Select):
    template_name = 'font_icons/select.html'
