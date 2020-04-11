from django import template
from MyWatchList.models import WatchList

register = template.Library()

@register.inclusion_tag("List/tags/statistic.html")
def SerialsStatic(profile):


    return {
        'profile': profile,
        'urlname': "listserial",
        'section': "Сериалы",
        'mainclass': "serials",
        "lowcolor": "#778beb",
        "highcolor": "#546de5",
        "item": Movie(profile, WatchList.manager.get_series())
    }

@register.inclusion_tag("List/tags/statistic.html")
def FilmStatic(profile):

    return {
        'profile': profile,
        'urlname': "listfilm",
        'section': "Фильмы",
        'mainclass': "films",
        "lowcolor": "#e77f67",
        "highcolor": "#e15f41",
        "item": Movie(profile,WatchList.manager.get_films())
    }

class MovieElem:
    count = 0
    width = ""

    def __init__(self, count, one):
        self.count = count
        self.width = str( one * count).replace(",", ".")



class Movie:
    watched = None
    planned = None
    watch = None

    def __init__(self, profile, query):
        from MyWatchList.views.list.userstatus import UserStat
        from django.db.models import Q
        all = query.filter(user=profile.user)

        planned = all.filter(userstatus=UserStat['planned']['id']).count()
        watch = all.filter(Q(userstatus=UserStat['watch']['id']) | Q(userstatus=UserStat['rewatch']['id'])).count()
        watched = all.filter(userstatus=UserStat['watched']['id']).count()

        try:
            one = 100 / (planned + watch + watched)
        except ZeroDivisionError:
            one = 100
        self.watch = MovieElem(watch, one)
        self.planned = MovieElem(planned, one)
        self.watched = MovieElem(watched, one)
        del one, planned, watch, watched, all
