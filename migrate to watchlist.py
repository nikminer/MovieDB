from Main import models
from MyWatchList import models as WLmodels


for i in models.Serial.objects.all():
    movie=WLmodels.Movie.objects.create(name=i.name, originalname=i.originalname,length=i.episodelength,year=i.year,kinopoiskid=i.kinopoiskid,img=i.img, rating=i.rating, series=True)
    movie.disctiption= models.Season.objects.filter(serial=i).first().disctiption
    for tag in i.tags.names():
        movie.tags.add(tag)
    movie.save()

    for seas in models.Season.objects.filter(serial=i):
        season = WLmodels.Season.objects.create(movie=movie, rating=seas.rating, status_id=seas.status.id,name=seas.name,episodecount=seas.episodecount,position=seas.position,img=seas.img,  disctiption=seas.disctiption)
        for ser in models.SeriesList.objects.filter(season=seas):
            WLmodels.SeriesList.objects.create(season=season, name=ser.name, date=ser.date)

        for ul in models.UserList.objects.filter(serial=i,season=seas):
            WLmodels.WatchList.objects.create(user=ul.user, movie=movie, season=season, userrate=ul.userrate,
                                                  userstatus=ul.userstatus, rewatch=ul.countreview,
                                                  userepisode=ul.userepisode, updated=ul.updated)

for i in models.Film.objects.all():
    movie=WLmodels.Movie.objects.create( name=i.name, originalname=i.originalname,length=i.length,year=i.year,kinopoiskid=i.kinopoiskid,img=i.img, rating=i.rating,disctiption=i.disctiption)
    for tag in i.tags.names():
        movie.tags.add(tag)
    movie.save()
    for ul in models.UserListF.objects.filter(film=i):
        WLmodels.WatchList.objects.create(user=ul.user,movie=movie, userrate=ul.userrate, userstatus=ul.userstatus, rewatch=ul.countreview, updated=ul.updated)
