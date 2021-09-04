from django import template

from MyWatchList.models import WatchList
from MyWatchList.models import SeriesList

register = template.Library()

@register.inclusion_tag("Serials/blocks/Following.html")
def followingListS(profile,season):
    return {
        'following': WatchList.objects.filter(
            user__profile__in=profile.following.all(),
            season=season
        ).order_by('user__first_name')
    }

@register.inclusion_tag("Serials/blocks/SeriesList.html")
def serieslist(season):
    return {
        'episodes': SeriesList.objects.filter(season=season)
            .order_by('date')
    }