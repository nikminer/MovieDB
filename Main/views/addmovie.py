import django
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from Main.models import Serial,Season,SeriesList,Film
from taggit.models import Tag
from kinopoisk.movie import Movie
from django.db.models import Q
from requests import get
import datetime
import re


@login_required
def AddMoviePage(request):
    return render(request,"Main/addmovie.html")

@login_required
def Search(request):
    serials={}
    films={}
    for i in Movie.objects.search(request.POST['name']):
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

    movie= Movie(id=id)
    movie.get_content('main_page')
    movie.get_content("series")

    if movie.series:
        serial=AddSerial(movie)
        AddGenres(movie,serial)
        AddSeasons(movie,serial.id)
        AddPoster(serial)
        return redirect('serial',serial.id)
    else:
        film=AddFilm(movie)
        AddGenres(movie,film)
        AddPoster(film)
        return redirect('film',film.id)

def checkID(id):
    try:
        return redirect('serial',Serial.objects.get(kinopoiskid=id).id)
    except Serial.DoesNotExist:
        try:
            return redirect('film',Film.objects.get(kinopoiskid=id).id)
        except Film.DoesNotExist:
            return None
        
def AddFilm(movie):
    newfilm=Film.objects.create(name=movie.title,kinopoiskid=movie.id,year=movie.year,length=movie.runtime,disctiption=movie.plot)
    if not movie.title_en:
        newfilm.originalname=movie.title
    else:
        newfilm.originalname=movie.title_en

    newfilm.save()

    return newfilm

def AddPoster(movie):
    from django.core.files import File
    from django.core.files.temp import NamedTemporaryFile
    url="https://st.kp.yandex.net/images/film_big/"+str(movie.kinopoiskid)+".jpg"
    img_temp = NamedTemporaryFile()
    img_temp.write(get(url).content)
    img_temp.flush()
    movie.img.save(str(movie.id)+"."+url.split('.')[-1],img_temp)


def AddSerial(movie):
    newserial=Serial.objects.create(name=movie.title,kinopoiskid=movie.id,year=movie.year,episodelength=movie.runtime)
    if not movie.title_en:
        newserial.originalname=movie.title
    else:
        newserial.originalname=movie.title_en

    newserial.name=re.sub(r"[(]сериал\s*[)]","",newserial.name,count=1)

    newserial.img="https://st.kp.yandex.net/images/film/"+str(movie.id)+".jpg"
    newserial.save()

    return newserial

def AddGenres(movie,obj):
    print(movie.genres,Tag.objects.filter(name__in= movie.genres))
    for i in Tag.objects.filter(name__in= movie.genres):
        obj.tags.add(i)


def AddSeasons(movie,id):
    for i in range(0,len(movie.seasons)):
        season=Season.objects.create(name=str(i+1)+" сезон",episodecount=len(movie.seasons[i].episodes),serial_id=id)
        if i==0:
            season.disctiption=movie.plot
        
        cdate = datetime.date.today()
        try:
            if movie.seasons[i].episodes[-1].release_date > cdate:
                season.status_id=2
            else:
                season.status_id=3
        except:
            season.status_id=2
        
        try:
            if movie.seasons[i].episodes[0].release_date > cdate:
                season.status_id=1
        except TypeError:
            season.status_id=1
        season.save()
        
        AddEpisodes(movie.seasons[i].episodes,season)
        
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