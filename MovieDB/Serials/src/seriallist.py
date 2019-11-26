from django.shortcuts import render
from Main.models import Series,UserListS,Season,SeriesList
import os,re
import datetime
from django.db.models import Q

def SerialList(request):
    
    seriesList=[]

    for i in Series.objects.all():
        try:
            firstdate=SeriesList.objects.filter(
                season=Season.objects.filter(series=i).order_by('-id').first()
            ).first().date
        except AttributeError:
            firstdate=datetime.date(1900, 1, 1)
        
        series=MetaSerial(i,firstdate)
        series.InMyList=str(len(UserListS.objects.filter(movie=i.movie,user=request.user))>0)
        seriesList.append(series)


    data={
        "SeriesList":sorted(seriesList,key=lambda MetaSetial: MetaSetial.firstdate, reverse=True),
    }
    return render(request,"Serials/seriallist.html",data)

class MetaSerial:
    def __init__(self,series,firstdate):
        self.id=series.id
        self.movie=series.movie
        self.poster=series.poster
        self.firstdate=firstdate
    