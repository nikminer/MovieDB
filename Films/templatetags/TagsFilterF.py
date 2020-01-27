from django import template

from Main.models import Film


register = template.Library()
@register.inclusion_tag("Films/blocks/FilmsFilter.html")

def show_avalible_filtersF():
    return {
        'tags':Film.tags.all().order_by('name')
    }
