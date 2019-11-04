from django.shortcuts import render
from Main.models import UserList,Season,Genre,SeriesList
import os, re

def season(request,id):
    season=Season.objects.get(id=id)
    genre= Genre.objects.filter(serial=season.serial.id)
    try:
        season.date= SeriesList.objects.filter(season_id=id).order_by('date').first().date
    except AttributeError:
        season.date="Нет данных"

    episodes= SeriesList.objects.filter(season_id=id).order_by('date')
    data={
        "season":season,
        "genre":genre,
        "episodes":episodes
    }
    try:
        data.update({"UserItem":UserList.objects.get(season=season,user=request.user.id)})
    except UserList.DoesNotExist:
        pass

    return render(request,"Serials/season.html",data)