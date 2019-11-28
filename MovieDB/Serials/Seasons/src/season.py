from django.shortcuts import render, get_object_or_404
from Main.models import UserListS,Season,Genre,SeriesList
import os, re

def season(request,id):
    season=get_object_or_404(Season,id=id)
    try:
        season.date= SeriesList.objects.filter(season=season).order_by('date').first().date
    except AttributeError:
        season.date="Нет данных"

    episodes= SeriesList.objects.filter(season=season).order_by('date')
    data={
        "season":season,
        "episodes":episodes
    }
    try:
        data.update({"UserItem":UserListS.objects.get(season=season,user=request.user)})
    except UserListS.DoesNotExist:
        pass

    return render(request,"Serials/season.html",data)