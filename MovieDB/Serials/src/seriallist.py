from django.shortcuts import render
from Main.models import Series,UserListS,Season,SeriesList
import os,re
import datetime

def SerialList(request):
    
    SerialList=[]

    for i in Series.objects.all():
        try:
            firstdate=SeriesList.objects.filter(season_id=Season.objects.filter(movie=i.movie).order_by('-id').first().id).first().date
        except AttributeError:
            firstdate=datetime.date(1900, 1, 1)
        

        serial=MetaSerial(i,firstdate)
            
        serial.InMyList=str(len(UserListS.objects.filter(movie=i.movie,user=request.user))>0)
        SerialList.append(serial)


    data={
        "SerialList":sorted(SerialList,key=lambda MetaSetial: MetaSetial.firstdate, reverse=True),
    }
    return render(request,"Serials/seriallist.html",data)

class MetaSerial:
    def __init__(self,Serial,firstdate):
        self.id=Serial.id
        self.name=Serial.name
        self.originalname=Serial.originalname
        self.year=Serial.year
        self.firstdate=firstdate
        self.img=Serial.img