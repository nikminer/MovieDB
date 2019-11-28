import django
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from Main.models import Series,Season,GenreList,Genre,SeriesList,Film, Movie,Posters
from kinopoisk.movie import Movie as KinoMovie
from django.db.models import Q
from requests import get
import datetime
import re
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile



@login_required
def AddMoviePage(request):
    return render(request,"Main/addmovie.html")

@login_required
def Search(request):
    serials={}
    films={}
    for i in KinoMovie.objects.search(request.POST['name']):
        if (i.series):
            serial={"id":i.id,"name":i.title,"year":i.year,"poster":"https://st.kp.yandex.net/images/film/"+str(i.id)+".jpg"}
            if i.title_en:
                serial.update({"originalname":i.title_en})
            serials.update({i.id:serial})
        else:
            film={"id":i.id,"name":i.title,"year":i.year,"poster":"https://st.kp.yandex.net/images/film/"+str(i.id)+".jpg"}
            if i.title_en:
                film.update({"originalname":i.title_en})
            films.update({i.id:film})

    return JsonResponse({
        'serials':{'result':serials,"length":len(serials)},
        'films':{'result':films,"length":len(films)}
    })





@login_required
def AddMovie(request,id):
    chkres=checkID(id)
    if chkres:
        return chkres


    kinomovie= KinoMovie(id=id)
    kinomovie.get_content('main_page')
    try:
        kinomovie.get_content("series")
    except UnboundLocalError:
        pass
    #kinomovie.get_content("posters")
    
    movie= AddMovieFunc(kinomovie)
    AddGenres(kinomovie,movie)
    #AddPosters(kinomovie,movie)

    if not kinomovie.series:
        return redirect('film',AddFilm(movie,kinomovie).id)
    else:
        series=AddSerial(movie,kinomovie)
        AddSeasons(kinomovie,series)
        return redirect('serial',series.id)
        

def checkID(id):
    try:
        return redirect('serial',Series.objects.get(movie__kinopoiskid=id).id)
    except Series.DoesNotExist:
        try:
            return redirect('film',Film.objects.get(movie__kinopoiskid=id).id)
        except Film.DoesNotExist:
            return None
    
def AddMovieFunc(kinomovie):
    movie= Movie.objects.create(
        name=kinomovie.title,
        originalname= kinomovie.title if not kinomovie.title_en else kinomovie.title_en,
        kinopoiskid=kinomovie.id,
        year=kinomovie.year,
        length=kinomovie.runtime,
        disctiption=kinomovie.plot
    )
    if kinomovie.series:
        movie.name=re.sub(r"[(]сериал\s*[)]","",movie.name,count=1)
        movie.save()

    return movie

def AddGenres(kinomovie,movie):
    for i in kinomovie.genres:
        try:
            Genre.objects.create(genre=GenreList.objects.get(name=i),movie=movie)
        except GenreList.DoesNotExist:
            pass

def AddPosters(kinomovie,movie):
    for i in kinomovie.posters:
        poster=Posters.objects.create(movie=movie)

        img_temp = NamedTemporaryFile()
        img_temp.write(get(i).content)
        img_temp.flush()

        poster.img.save(str(kinomovie.id)+"."+i.split('.')[-1],img_temp)
        poster.save()

def AddPoster(kinomovie,movie,url):
    poster=Posters.objects.create(movie=movie)

    img_temp = NamedTemporaryFile()
    img_temp.write(get(url).content)
    img_temp.flush()

    poster.img.save(str(kinomovie.id)+"."+url.split('.')[-1],img_temp)
    poster.save()
    return poster

def AddFilm(movie,kinomovie):
    return Film.objects.create(
        movie=movie,
        poster= AddPoster(kinomovie,movie,"https://st.kp.yandex.net/images/film/"+str(kinomovie.id)+".jpg")
    )

def AddSerial(movie,kinomovie):
    return Series.objects.create(
        movie=movie,
        poster= AddPoster(kinomovie,movie,"https://st.kp.yandex.net/images/film/"+str(kinomovie.id)+".jpg")
    )
    


def AddSeasons(kinomovie,series):
    
    for i in range(0,len(kinomovie.seasons)):

        season= Season.objects.create(
            name=str(i+1)+" сезон",
            episodecount=len(kinomovie.seasons[i].episodes),
            series=series
        )

        #set discript first season
        if i==0:
            season.disctiption=kinomovie.plot
            season.poster= Posters.objects.filter(movie=series.movie).first()

        #set season status
        cdate = datetime.date.today()
        try:
            if kinomovie.seasons[i].episodes[-1].release_date > cdate:
                season.status_id=2
            else:
                season.status_id=3
        except:
            season.status_id=2
        try:
            if kinomovie.seasons[i].episodes[0].release_date > cdate:
                season.status_id=1
        except TypeError:
            season.status_id=1

        season.save()

        AddEpisodes(kinomovie.seasons[i].episodes,season)
        
def AddEpisodes(episodes,season):
    rdate=None
    for i in range(0,len(episodes)):
        if episodes[i].title:
            SeriesList.objects.create(
                name=str(episodes[i].title),
                date=episodes[i].release_date,
                season=season
            )
            rdate=datetime.datetime.strptime(str(episodes[i].release_date),"%Y-%m-%d")
        else:
            if rdate:
                rdate+=datetime.timedelta(days=7)
                SeriesList.objects.create(
                    name=str(i+1)+" серия",
                    date=str(rdate.date()),
                    season=season
                )