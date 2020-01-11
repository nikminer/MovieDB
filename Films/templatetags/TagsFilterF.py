from django import template

from Main.models import GenreF,GenreList


register = template.Library()
@register.inclusion_tag("Films/blocks/FilmsFilter.html")

def show_avalible_filtersF():
    return {
        'tags':GenreList.objects.filter(genref__in=GenreF.objects.all()).distinct().order_by('name')
    }
