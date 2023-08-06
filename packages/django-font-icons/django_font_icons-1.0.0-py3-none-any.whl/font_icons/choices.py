from django.utils.translation import ugettext_lazy as _
from djchoices import ChoiceItem, DjangoChoices


class StyleChoices(DjangoChoices):
    fa = ChoiceItem('fa', _('Font Awesome (classic)'))
    fas = ChoiceItem('fas', _("Font Awesome Solid"))
    far = ChoiceItem('far', _("Font Awesome Regular (Partial Pro)"))
    fal = ChoiceItem('fal', _("Font Awesome Light (Pro)"))
    fab = ChoiceItem('fab', _("Font Awesome Brands"))
