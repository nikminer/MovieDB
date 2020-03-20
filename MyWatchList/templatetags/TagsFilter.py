from django import template

from Main.models import Serial


register = template.Library()
@register.inclusion_tag("Serials/blocks/SerialFilter.html")
def show_avalible_filters():
    return {
        'tags':Serial.tags.all().order_by('name')
    }
