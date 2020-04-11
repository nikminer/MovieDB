from django import template

from MyWatchList.models import Movie


register = template.Library()
@register.inclusion_tag("Serials/blocks/SerialFilter.html")
def show_avalible_filters():
    return {
        'tags': Movie.tags.filter(movie__series=True).order_by('name')
    }

@register.inclusion_tag("Films/blocks/FilmsFilter.html")
def show_avalible_filtersF():
    return {
        'tags': Movie.tags.filter(movie__series=False).order_by('name')
    }