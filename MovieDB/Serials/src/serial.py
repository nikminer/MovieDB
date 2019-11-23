from django.shortcuts import render,get_object_or_404
from Main.models import Series,Genre,Season,UserListS,SeriesList
import os,re
from django.contrib.auth.decorators import login_required

def serial(request,id):
    serial=get_object_or_404(Serial,movie_id=id)
        
    fseason=serial.seasons.first()
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
        "fseason":fseason
    }
    
    try:
        data.update({"UserItem":UserListS.objects.filter(movie=serial.movie,user=request.user.id)})
    except UserList.DoesNotExist:
        pass
        
    return render(request,"Serials/serial.html",data)

class Fseason():
    disctiption="Нет данных"
    date="Нет данных"