from django.shortcuts import render
from Main.models import Film,UserListF

import os,re
import datetime

def FilmList(request):
    

    FilmList= Film.objects.all().order_by('movie__year').reverse()
    for film in FilmList:
        film.InMyList=str(len(UserListF.objects.filter(movie=film.movie,user=request.user.id))>0)
        
    data={
        "FilmList":FilmList,
    }
    return render(request,"Films/filmlist.html",data)