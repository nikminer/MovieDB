from Main.models import SeriesList,Serial,Season
from List.models import UserList
from Profile.views.notifications import addnotification
from kinopoisk.movie import Movie
import datetime

def checkSeries():
  for i in SeriesList.objects.filter(date=datetime.datetime.today() - datetime.timedelta(days=1)):
    for profile in UserList.objects.filter(season=i.season):
      addnotification("Вышла новая серия {}".format(i.name),i.season.serial,profile.user.profile)

def checkStatus():
  for season in Season.objects.filter(status=2):
    series=SeriesList.objects.filter(season=season)
    if series.count() == season.episodecount:
      if not series.filter(date__gt=datetime.datetime.today()).exists():
        season.status_id=3
        season.save()
        for profile in UserList.objects.filter(season=season):
          addnotification("Релиз  {}".format(season.name),season.serial,profile.user.profile)
      else:
          addnotification("{} Series list and Episode count not equal".format(season.name),season.serial,Profile.objects.get(id=1))
