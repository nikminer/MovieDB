from django.shortcuts import render
from Main.models import Serial,UserList,Season,SeriesList
import os,re
import datetime

def SerialList(request):
    
    SerialList=[]

    for i in Serial.objects.all():
        try:
            firstdate=SeriesList.objects.filter(season_id=Season.objects.filter(serial_id=i.id).order_by('-id').first().id).first().date
        except AttributeError:
            firstdate=datetime.date(1900, 1, 1)
        

        serial=MetaSerial(i,firstdate)
            
        serial.InMyList=str(len(UserList.objects.filter(serial=i.id,user=request.user.id))>0)
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