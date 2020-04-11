from . import watchlistitems

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from MyWatchList.views.list.userstatus import UserStat

from MyWatchList.models import WatchList, Movie



@login_required
def watchlist_series(request, username=None):

    if not username:
        user = request.user
    else:
        user = get_object_or_404(User, username=username)

    userlist = filter(request, WatchList.objects.filter(movie__in=Movie.manager.get_series(), user=user).order_by('movie__name'))

    lists = dict()
    for i in UserStat.items():
        lists.update({
            i[0]: {
                "name": i[1]['name'],
                "list": getSeasonslist(userlist, i[1]['id']),
            }
        })

    data={
        "user": user,
        "groups": lists,
        "genrelist": genrelist(Movie.manager.get_seriesByUser(user)),
        "series": True
    }

    return render(request,"List/list.html",data)


@login_required
def watchlist_films(request,username):
    if not username:
        user=request.user
    else:
        user= get_object_or_404(User, username=username)
    
    userlist = filter(request,WatchList.objects.filter(movie__in=Movie.manager.get_films(), user=user))
    
    lists={}
    for i in UserStat.items():
        lists.update({
            i[0]: {
                "name": i[1]['name'],
                "list": getFilmsList(userlist, i[1]['id']),
            }
        })

    return render(request,"List/list.html",{
        "groups":lists,
        "series": False,
        "genrelist":genrelist(Movie.manager.get_filmsByUser(user)),
        "user":user
    })


@login_required
def addlist(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if movie.series:
        for i in movie.get_seasons():
            WatchList.objects.get_or_create(user=request.user, movie=movie, season=i)

        return redirect('listserial', request.user.username)
    else:
        WatchList.objects.create(user=request.user, movie=movie)
        return redirect('listfilm', request.user.username)

@login_required
def dellist(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    for i in WatchList.objects.filter(user=request.user, movie=movie):
        i.delete()

    if movie.series:
        return redirect('seriallist')
    else:
        return redirect('filmlist')




def getSeasonslist(list, status):
    structlist = {}
    for item in list.filter(userstatus=status):
        movie = structlist.get(item.movie)
        if movie:
            movie.append(item)
            structlist.update({item.movie: movie})
        else:
            structlist.update({item.movie: [item]})
    return structlist

def getFilmsList(list,status):
    structlist = {}
    for item in list.filter(userstatus=status):
        structlist.update({item.movie:item})
    return structlist


def filter(request,list):
    if request.GET.get('genres'):
        list = list.filter(movie__tags__slug__in=request.GET.get('genres').split(' '))
    
    return list

def genrelist(list):
    genrelist={}
    for item in list:
        for tag in item.tags.all():
            if genrelist.get(tag):
                genrelist[tag] += 1
            else:
                genrelist.update({tag: 1})
    return dict(sorted(genrelist.items()))