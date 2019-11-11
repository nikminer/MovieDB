from django.shortcuts import render
from Main.models import Serial,Genre,Season,UserList,SeriesList
import os,re
from django.contrib.auth.decorators import login_required

def serial(request,id):
    serial=Serial.objects.get(id=id)
        
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
        data.update({"UserItem":UserList.objects.filter(serial=id,user=request.user.id)})
    except UserList.DoesNotExist:
        pass
        
    return render(request,"Serials/serial.html",data)

class Fseason():
    disctiption="Нет данных"
    date="Нет данных"