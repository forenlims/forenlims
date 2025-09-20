from typing import List, Tuple

from django import template
from django.conf import settings

register = template.Library()
@register.simple_tag
def get_languages()-> List[Tuple[str, str]]:
    return settings.LANGUAGES
