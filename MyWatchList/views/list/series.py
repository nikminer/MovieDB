from django.shortcuts import render,redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.db.models import Count
from List.views.userstatus import UserStat

from MyWatchList.models import WatchList,Movie,Season



@login_required
def watchlist(request, username=None):

    if not username:
        user = request.user
    else:
        user = User.objects.get(username=username)

    list = WatchList.objects.filter(movie__in=Movie.manager.get_series(), user=user)

    lists={}



    for i in UserStat.items():
        lists.update({
            i[0]: {
                "name": i[1]['name'],
                "list": getSeriesllist(list, i[1]['id'], request),
            }
        })

    genrelist={}
    for item in Movie.manager.get_seriesByUser(user):
        for tag in item.tags.all():
            if genrelist.get(tag):
                genrelist[tag]+=1
            else:
                genrelist.update({tag: 1})

    data={
        "user": user,
        "groups": lists,
        "genrelist": dict(sorted(genrelist.items())),
    }

    return render(request,"List/list.html",data)

def getSeriesllist(list, status, request):

    if request.GET.get('genres'):
        list = list.filter(movie__tags__slug__in=request.GET.get('genres').split(' '))

    structlist = {}
    for item in list.filter(userstatus=status):
        movie = structlist.get(item.movie)
        if movie:
            movie.append(item)
            structlist.update({item.movie: movie})
        else:
            structlist.update({item.movie: [item]})
    return structlist


'''
@login_required
def AddSerial(request, id):
    seasons = []
    for i in UserList.objects.filter(serial=id, user=request.user.id):
        seasons.append(i.season)
    for season in Season.objects.filter(serial=id):
        if not season in seasons:
            UserList.objects.create(user_id=request.user.id, season_id=season.id, serial_id=id, userstatus=1)
    return redirect('listserial', request.user.username)


@login_required
def DelSerial(request, id):
    UserList.objects.filter(serial=id, user=request.user.id).delete()
    return redirect('listserial', request.user.username)
'''