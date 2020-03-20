from django import template
from Profile.models import Friendlist
from MyWatchList.models import Movie, WatchList

register = template.Library()

@register.inclusion_tag("Films/blocks/Friends.html")
def friendListF(profile, film):
    return {
        'friends': WatchList.objects.filter(
            user__in=Friendlist.friends.get_friends(profile),
            movie=film
        ).order_by('user__first_name')
    }


@register.inclusion_tag("Films/tags/similar_films.html")
def SimilarFilms(movie):
    from django.db.models import Count
    tags_ids = movie.tags.values_list('id', flat=True)
    similar = Movie.manager.get_films().filter(tags__in=tags_ids) \
        .exclude(id=movie.id)

    similar = similar.annotate(same_tags=Count('tags')) \
        .order_by('-same_tags', '-rating')[:5]

    return {
        "similar": similar,
        "film": movie,
    }
