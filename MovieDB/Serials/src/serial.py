from django.shortcuts import render
from Main.models import Serial,Genre,Season,UserList,SeriesList
import os,re
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

def serial(request,id):
    serial=Serial.objects.get(id=id)
    
    genre= Genre.objects.filter(serial=id)

    seasons= Season.objects.filter(serial=id)

    raring=Season.objects.filter(serial=id).filter(rating__gt=0).aggregate(Avg('rating'))['rating__avg']
    if not raring:
        raring=0.00
        
    fseason=seasons.first()
    if (fseason):
        try:
            fseason.date=SeriesList.objects.filter(season_id=fseason.id).order_by('date').first().date
        except AttributeError:
            dsicript=fseason.disctiption
            fseason=Fseason()
            fseason.disctiption=dsicript
    else:
        fseason=Fseason()
    
    data={
        "serial":serial,
        "genre":genre,
        "seasons":seasons,
        "rating":round(raring,2),
        "fseason":fseason
    }
    
    try:
        data.update({"UserItem":UserList.objects.filter(serial=id,user=request.user.id)})
    except UserList.DoesNotExist:
        pass
        
    return render(request,"Serials/serial.html",data)


class Fseason():
    disctiption="Нет данных"
    date="Нет данных"