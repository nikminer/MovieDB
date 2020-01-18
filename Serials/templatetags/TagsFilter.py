from django import template

from Main.models import Genre,GenreList


register = template.Library()
@register.inclusion_tag("Serials/blocks/SerialFilter.html")

def show_avalible_filters():
    return {
        'tags':GenreList.objects.filter(genre__in=Genre.objects.all()).distinct().order_by('name')
    }
