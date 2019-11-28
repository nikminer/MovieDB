from django.shortcuts import render,get_object_or_404
from Main.models import Series,Genre,Season,UserListS,SeriesList
import os,re
from django.contrib.auth.decorators import login_required

def serial(request,id):
    series=get_object_or_404(Series,movie_id=id)
        
    fseason=series.seasons.first()
    if (fseason):
        try:
            fseason.date=SeriesList.objects.filter(season=fseason).order_by('date').first().date
        except AttributeError:
            dsicript=fseason.disctiption
            fseason=Fseason()
            fseason.disctiption=dsicript
    else:
        fseason=Fseason()
    
    data={
        "series":series,
        "fseason":fseason
    }
    
    try:
        data.update({"UserItem":UserListS.objects.filter(movie=series.movie,user=request.user)})
    except UserList.DoesNotExist:
        pass
        
    return render(request,"Serials/serial.html",data)

class Fseason():
    disctiption="Нет данных"
    date="Нет данных"