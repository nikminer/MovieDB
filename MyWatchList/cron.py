from MyWatchList.models import SeriesList, Season, WatchList
from Profile.views.notifications import addnotification

import datetime

def checkSeries():
    for i in SeriesList.objects.filter(date=datetime.datetime.today() - datetime.timedelta(days=1)):
        for wl in WatchList.objects.filter(season=i.season):
            addnotification("Вышла новая серия {}".format(i.name), i.season.serial, wl.user.profile)

def checkStatus():
    for season in Season.objects.filter(status=2):
        series = SeriesList.objects.filter(season=season)
        if series.count() == season.episodecount:
            if not series.filter(date__gt=datetime.datetime.today()).exists():
                season.status_id = 3
                season.save()
                for profile in WatchList.objects.filter(season=season):
                    addnotification("Релиз  {}".format(season.name), season.serial, profile.user.profile)