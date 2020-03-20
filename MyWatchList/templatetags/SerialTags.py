from django import template
from MyWatchList.models import Movie

register = template.Library()

@register.inclusion_tag("Serials/tags/similar_serials.html")
def SimilarSeries(movie:Movie):
    from django.db.models import Count
    tags_ids = movie.tags.values_list('id', flat=True)
    similar = Movie.manager.get_series().filter(tags__in=tags_ids) \
        .exclude(id=movie.id)

    similar = similar.annotate(same_tags=Count('tags')) \
        .order_by('-same_tags', '-rating')[:5]

    return {
        "similar": similar,
        "series": movie,
    }

@register.inclusion_tag("Serials/tags/date_tag.html")
def SeriesDate(movie:Movie):
    return {
        "date": movie.get_seasons().first().get_date(),
    }
