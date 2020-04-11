from MyWatchList.models import SeriesList, Season, WatchList
from Profile.views.notifications import addnotification

import datetime

def checkSeries():
    for i in SeriesList.objects.filter(date=datetime.datetime.today()):
        for wl in WatchList.objects.filter(season=i.season):
            addnotification("Вышла новая серия {}".format(i.name), wl.user.profile, obj=i.season)

def checkStatus():
    for season in Season.objects.filter(status=2):
        series = SeriesList.objects.filter(season=season)
        if series.count() == season.episodecount:
            if not series.filter(date__gt=datetime.datetime.today()).exists():
                season.status_id = 3
                season.save()
                for profile in WatchList.objects.filter(season=season):
                    addnotification("Релиз  {}".format(season.name), profile.user.profile, obj=season)