from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from MyWatchList.views.decoratiors import ajax_required
from MyWatchList.models import Season, SeriesList, Movie
from taggit.models import Tag
from kinopoisk.movie import Movie as KPMovie
from requests import get
import datetime
import re


@login_required
def AddMoviePage(request):
    return render(request, "Main/addmovie.html")


@ajax_required
@login_required
def Search(request):
    serials = {}
    films = {}
    for i in KPMovie.objects.search(request.POST['name']):
        if (i.series):
            serial = {"id": i.id, "name": i.title, "year": i.year,
                      "poster": "https://st.kp.yandex.net/images/film_big/" + str(i.id) + ".jpg"}
            if i.title_en:
                serial.update({"originalname": i.title_en})
            serials.update({i.id: serial})
        else:
            film = {"id": i.id, "name": i.title, "year": i.year,
                    "poster": "https://st.kp.yandex.net/images/film_big/" + str(i.id) + ".jpg"}
            if i.title_en:
                film.update({"originalname": i.title_en})
            films.update({i.id: film})

    return render(request, "Main/blocks/addmovie_searchlist.html", {
        'series': serials,
        'films': films
    })


@login_required
def AddMovie(request, id):
    if Movie.objects.filter(kinopoiskid=id).exists():
        return redirect(Movie.objects.get(kinopoiskid=id).get_absolute_url())

    movie = KPMovie(id=id)
    movie.get_content('main_page')
    movie.get_content("series")
    newmovie = Movie.objects.create(
            name=movie.title,
            kinopoiskid=movie.id,
            year=movie.year,
            length=movie.runtime,
            disctiption=movie.plot
        )
    if not movie.title_en:
        newmovie.originalname = movie.title
    else:
        newmovie.originalname = movie.title_en

    newmovie.name = re.sub(r"[(]сериал\s*[)]", "", newmovie.name, count=1)

    if movie.series:
        AddSeasons(movie, newmovie)

    AddGenres(movie, newmovie)
    AddPoster(newmovie)


    return redirect(newmovie.get_absolute_url())


def AddPoster(movie):
    from django.core.files.temp import NamedTemporaryFile
    url = "https://st.kp.yandex.net/images/film_big/" + str(movie.kinopoiskid) + ".jpg"
    img_temp = NamedTemporaryFile()
    img_temp.write(get(url).content)
    img_temp.flush()
    movie.img.save(str(movie.id) + "." + url.split('.')[-1], img_temp)

def AddGenres(movie, obj):
    for i in Tag.objects.filter(name__in=movie.genres):
        obj.tags.add(i)



def AddSeasons(movie, id):
    for i in range(0, len(movie.seasons)):
        season = Season.objects.create(name=str(i + 1) + " сезон", episodecount=len(movie.seasons[i].episodes),
                                       serial_id=id)
        if i == 0:
            season.disctiption = movie.plot

        cdate = datetime.date.today()
        try:
            if movie.seasons[i].episodes[-1].release_date > cdate:
                season.status_id = 2
            else:
                season.status_id = 3
        except:
            season.status_id = 2

        try:
            if movie.seasons[i].episodes[0].release_date > cdate:
                season.status_id = 1
        except TypeError:
            season.status_id = 1
        season.save()

        AddEpisodes(movie.seasons[i].episodes, season)


def AddEpisodes(episodes, season):
    rdate = None
    for i in range(0, len(episodes)):
        if episodes[i].title:
            SeriesList.objects.create(
                name=str(episodes[i].title),
                date=episodes[i].release_date,
                season=season
            )
            rdate = datetime.datetime.strptime(str(episodes[i].release_date), "%Y-%m-%d")
        else:
            if rdate:
                rdate += datetime.timedelta(days=7)
                SeriesList.objects.create(
                    name=str(i + 1) + " серия",
                    date=str(rdate.date()),
                    season=season
                )

