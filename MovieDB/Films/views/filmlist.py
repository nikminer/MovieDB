from django.shortcuts import render
from Main.models import Film,UserListF,GenreList

import os,re
import datetime

def FilmList(request):
    FilmList=Film.objects.all().order_by('-year') 

    if request.GET.get('genres'):
       FilmList= FilmList.filter(genref__genre__tag__in=request.GET.get('genres').split(' ')).distinct()



    for film in FilmList:
        film.InMyList=str(len(UserListF.objects.filter(film=film,user=request.user))>0)
    
    data={
        "FilmList":FilmList,
        "Genrelist":GenreList.objects.all().order_by("name"),
    }
    return render(request,"Films/filmlist.html",data)