from django.shortcuts import render,redirect,get_object_or_404
from Main.models import UserListS,Season,Series,Genre,Movie
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 

from List.views.userstatus import UserStat


@login_required
def AddSerial(request,id):
    series = get_object_or_404(Series, id=id)
    seasons=UserListS.objects.filter(movie=series.movie,user=request.user).values_list('season')

    for season in Season.objects.filter(series=series):
        if not season in seasons:
            UserListS.objects.create(movie=series.movie,user=request.user,season=season)
    
    return redirect('listserial',request.user.username)
    
@login_required
def DelSerial(request,id):
    series = get_object_or_404(Series, id=id)
    UserListS.objects.filter(movie=series.movie,user=request.user).delete()
    return redirect('listserial',request.user.username)


@login_required
def userlist(request,username=None):
    if not username:
        user=request.user
    else:
        user=get_object_or_404(User,username=username)

    lists={}

    if request.GET.get('groups'):
        for i in request.GET.get('groups').split(' '):
            status=UserStat.get(i)
            if status:
                lists.update({
                    i:{
                        "name":status['name'],
                        "list":getSeriallist(user.id,status['id'],request),
                    }
                })
    else:
        for i in UserStat.items():
            lists.update({
                i[0]:{
                    "name":i[1]['name'],
                    "list":getSeriallist(user.id,i[1]['id'],request),
                }
            })


    genrelist={}

    for i in UserListS.objects.filter(user=user).only('movie').values_list('movie', flat=True).distinct():
        for genre in Movie.objects.get(id=i).genre:
            if genrelist.get(genre.genre.name):
                genrelist[genre.genre.name]['count'] += 1
            else:
                genrelist.update({genre.genre.name:{'count':1,'tag':genre.genre.tag}})
    
    genrelist=dict(sorted(genrelist.items()))
    return render(request,"List/list.html",{
        "groups":lists,
        "type":"series",
        "genrelist":genrelist,
    })


def getSeriallist(userid,statusid,request):
    serialDict={}
    userl=UserListS.objects.filter(user_id=userid,userstatus=statusid).order_by("movie__name")
    if request.GET.get('genres'):
        userl= userl.filter(
            movie__in=Genre.objects.filter(
                genre__tag__in=request.GET.get('genres').split(' '),
                movie__in=userl.values('movie')
            ).values('movie')
        )
    for i in userl:
        if not serialDict.get(i.season.series.id):
            item=SerialItem()
            item.seasons.append(i)
            item.movie=i.movie
            getUserProgress(item,i.movie.id,userid)

            serialDict.update({i.season.series.id:item})
        else:
            serialDict[i.season.series.id].seasons.append(i)
    
    return serialDict.values()

def getUserProgress(item,movieid,userid):
    userl=UserListS.objects.filter(user_id=userid,movie=movieid)
    item.episodes=0
    item.watched=0
    for i in userl:
        item.episodes+=i.season.episodecount
        item.watched+=i.userepisode

class SerialItem:
    movie=None
    seasons=[]
    episodes=0
    watched=0
    def __init__(self):
        self.movie=None
        self.seasons=[]