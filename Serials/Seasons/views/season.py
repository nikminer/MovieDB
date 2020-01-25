from django.shortcuts import render, get_object_or_404
from Main.models import UserList,Season,Genre,SeriesList

def season(request,id):
    season=get_object_or_404(Season,id=id)
    genre= Genre.objects.filter(serial=season.serial.id)
    try:
        season.date= SeriesList.objects.filter(season_id=id).order_by('date').first().date
    except AttributeError:
        season.date="Нет данных"


    data={
        "season":season,
        "genre":genre
    }
    try:
        data.update({"UserItem":UserList.objects.get(season=season,user=request.user.id)})
    except UserList.DoesNotExist:
        pass

    return render(request,"Serials/season.html",data)