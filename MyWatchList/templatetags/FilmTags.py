from django import template
from MyWatchList.models import Movie
from MyWatchList.models import WatchList

register = template.Library()

@register.inclusion_tag("Films/blocks/Following.html")
def followingListF(profile, movie):
    return {
        'following': WatchList.objects.filter(
            user__profile__in=profile.following.all(),
            movie=movie
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
