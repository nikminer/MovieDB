from django import template

from MyWatchList.models import Movie


register = template.Library()
@register.inclusion_tag("Films/blocks/FilmsFilter.html")

def show_avalible_filtersF():
    return {
        'tags':Movie.tags.all().order_by('name')
    }
