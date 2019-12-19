from django.shortcuts import render
from Main.models import Serial,UserList,Season,SeriesList,GenreList
import os,re
import datetime

def SerialList(request):
    
    Serials=Serial.objects.all().order_by("-year","name")


    if request.GET.get('genres'):
       Serials= Serials.filter(genre__genre__tag__in=request.GET.get('genres').split(' ')).distinct()
    
    for serial in Serials:
        serial.InMyList=str(len(UserList.objects.filter(serial=serial,user=request.user))>0)

    data={
        "SerialList":Serials,
        "Genrelist":GenreList.objects.all().order_by("name"),
    }
    
    return render(request,"Serials/seriallist.html",data)

