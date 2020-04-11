from django import template
from MyWatchList.models import WatchList, Movie
register = template.Library()

@register.inclusion_tag("Main/blocks/followers.html")
def followers(profile):

    return {
        'followers':profile.followers.count(),
        'followings':profile.following.count(),
        'profile':profile,
    }

@register.inclusion_tag("Main/blocks/MyLastFilms.html")
def MyLastFilms(profile):
    return {
        "films":WatchList.objects.filter(movie__in=Movie.manager.get_films(),user=profile.user).order_by('-updated')[:5],
        "username":profile.user.username
    }

@register.inclusion_tag("Main/blocks/MyLastSerials.html")
def MyLastSeries(profile):
    serials=[]
    for i in WatchList.objects.filter(user=profile.user, movie__in= Movie.manager.get_series()).order_by('-updated'):
        if i.movie not in serials:
            serials.append(i.movie)
            if len(serials)>=5:
                break
    return {
        "series":serials,
        "username":profile.user.username
    }