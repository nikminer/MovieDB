from django.shortcuts import render,redirect,get_object_or_404
from Main.models import UserListF,Movie,Genre
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 

from List.views.userstatus import UserStat

@login_required
def AddFilm(request,id):
    movie = get_object_or_404(Movie, id=id)    
    UserListF.objects.create(user=request.user,movie=movie)
    return redirect('listfilm',request.user.username)
    
@login_required
def DelFilm(request,id):
    movie = get_object_or_404(Movie, id=id)    
    UserListF.objects.filter(mvoie=movie,user=request.user).delete()
    return redirect('listfilm',request.user.username)


@login_required
def userlist(request,username):
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
                        "list":getFilmlist(user.id,status['id'],request),
                    }
                })
    else:
        for i in UserStat.items():
            lists.update({
                i[0]:{
                    "name":i[1]['name'],
                    "list":getFilmlist(user.id,i[1]['id'],request),
                }
            })
            
    genrelist={}
    for i in UserListF.objects.filter(user=user).only('movie').values_list('movie', flat=True).distinct():
        for genre in Movie.objects.get(id=i).genre:
            if genrelist.get(genre.genre.name):
                genrelist[genre.genre.name]['count'] += 1
            else:
                genrelist.update({genre.genre.name:{'count':1,'tag':genre.genre.tag}})
    genrelist=dict(sorted(genrelist.items()))

    return render(request,"List/list.html",{
        "groups":lists,
        "type":"films",
        "genrelist":genrelist,
    })

def getFilmlist(userid,statusid,request):
    userl=UserListF.objects.filter(user_id=userid,userstatus=statusid).order_by("movie__name")

    if request.GET.get('genres'):
        userl= userl.filter(
            movie__in=GenreF.objects.filter(
                genre__tag__in=request.GET.get('genres').split(' '),
                movie__in=userl.values('movie')
            ).values('movie')
        )

    return userl