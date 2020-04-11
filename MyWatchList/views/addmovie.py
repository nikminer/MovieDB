from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from MyWatchList.views.decoratiors import ajax_required
from MyWatchList.models import Season, SeriesList, Movie
from taggit.models import Tag
import tmdbsimple as tmdb
from requests import get
from datetime import datetime, timedelta
import re


@login_required
def AddMoviePage(request):
    return render(request, "Main/addmovie.html")


@ajax_required
@login_required
def Search(request):
    serials = {}
    films = {}
    search = tmdb.Search()
    search.tv(query=request.POST['name'], language="ru-RU")
    for i in search.results:
        serial = {"id": i['id'], "name": i['name']}

        if i['poster_path']:
            serial.update({"poster": "http://image.tmdb.org/t/p/w154" +i['poster_path']})
        else:
            serial.update({"poster": "/media/default.png" })

        try:
            serial.update({"year": datetime.strptime(i['first_air_date'], "%Y-%m-%d").year})
        except ValueError:
            serial.update({"year": i['first_air_date']})
        except KeyError:
            continue

        serial.update({"originalname": i['original_name']})
        serials.update({i['id']: serial})

    search.movie(query=request.POST['name'], language="ru-RU")
    for i in search.results:

        film = {"id": i['id'], "name": i['title']}

        try:
            film.update({"year": datetime.strptime(i['release_date'], "%Y-%m-%d").year})
        except ValueError:
            film.update({"year": i['release_date']})
        except KeyError:
            continue

        if i['poster_path']:
            film.update({"poster": "http://image.tmdb.org/t/p/w154" +i['poster_path']})
        else:
            film.update({"poster": "/media/default.png" })

        film.update({"originalname": i['original_title']})
        films.update({i['id']: film})


    return render(request, "Main/blocks/addmovie_searchlist.html", {
        'series': serials,
        'films': films
    })

@login_required
def AddMovie(request, id):
    if Movie.objects.filter(tmdbid=id).exists():
        return redirect(Movie.objects.get(tmdbid=id).get_absolute_url())
    movie = tmdb.Movies(id)
    movie.info(language="ru-RU")
    movie.releases()



    newmovie = Movie.objects.create(
        name=movie.title,
        originalname=movie.original_title,
        disctiption=movie.overview,
        
        release_date=datetime.strptime(movie.release_date, "%Y-%m-%d"),
        year=datetime.strptime(movie.release_date, "%Y-%m-%d").year,
        tmdbid=movie.id,
        imdbid=movie.imdb_id,

        length=movie.runtime,

    )
    
    
    for c in movie.countries:
        if c['iso_3166_1'] == 'US':
            newmovie.UScert=c['certification']
        if c['iso_3166_1'] == 'RU':
            newmovie.RUcert = c['certification']
            newmovie.release_dateRU= datetime.strptime(c['release_date'], "%Y-%m-%d")
    
    for i in movie.genres:
        newmovie.tags.add(i['name'])
    
    AddPoster(newmovie, movie.poster_path)
    
    
    return redirect(newmovie.get_absolute_url())


@login_required
def AddSeries(request, id):
    if Movie.objects.filter(tmdbid=id).exists():
        return redirect(Movie.objects.get(tmdbid=id).get_absolute_url())
    movie = tmdb.TV(id)
    movie.info(language="ru-RU")


    newmovie = Movie.objects.create(
        name=movie.name,
        originalname=movie.original_name,
        disctiption=movie.overview,

        release_date=datetime.strptime(movie.first_air_date, "%Y-%m-%d"),
        year=datetime.strptime(movie.first_air_date, "%Y-%m-%d").year,
        tmdbid=movie.id,
        series=True
    )
    if len(movie.episode_run_time) > 0:
        newmovie.length=movie.episode_run_time[0]

    for i in movie.genres:
        newmovie.tags.add(i['name'])

    AddPoster(newmovie, movie.poster_path)
    AddSeasons(movie, newmovie)
    return redirect(newmovie.get_absolute_url())



def AddPoster(movie, path):
    from django.core.files.temp import NamedTemporaryFile
    if path :
        url = "http://image.tmdb.org/t/p/original" + path
        img_temp = NamedTemporaryFile()
        img_temp.write(get(url).content)
        img_temp.flush()
        movie.img.save(str(movie.id) + "." + url.split('.')[-1], img_temp)


def AddSeasons(movie, newmovie):
    for i in movie.seasons:
        if i['air_date']:
            season = Season.objects.create(name=i['name'], episodecount=i['episode_count'],
                                           movie=newmovie, position=i['season_number'],tmdbid=i['id'])

            if len(i['overview'])>0:
                season.disctiption = i['overview']

            AddPoster(season, i['poster_path'])





            TVseason=tmdb.TV_Seasons(movie.id, i['season_number'])
            TVseason.info(language="ru-RU")
            AddEpisodes(TVseason,season.id)

            try:
                if datetime.strptime(TVseason.episodes[-1]['air_date'], "%Y-%m-%d") > datetime.today():
                    season.status_id = 2
                else:
                    season.status_id = 3
            except:
                season.status_id = 2

            try:
                if datetime.strptime(i['air_date'], "%Y-%m-%d") > datetime.today():
                    season.status_id = 1
            except TypeError:
                season.status_id = 1
            season.save()


def AddEpisodes(season,id):


    ldate = datetime.strptime(season.air_date, "%Y-%m-%d")
    for i in season.episodes:
        series = SeriesList.objects.create(
                name=str(i['name']),
                date=datetime.strptime(i['air_date'], "%Y-%m-%d") if i['air_date'] else ldate+timedelta(days=7),
                season_id=id
            )

        ldate= datetime.strptime(i['air_date'], "%Y-%m-%d") if i['air_date'] else ldate+timedelta(days=7)

        if len(i['overview'])>0:
            series.disctiption=i['overview']
        series.save()