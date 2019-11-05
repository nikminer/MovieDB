from django.shortcuts import render,redirect
from Main.models import UserListF
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 

from List.views.userstatus import UserStat

@login_required
def AddFilm(request,id):
    UserListF.objects.create(user_id=request.user.id,film_id=id,userstatus=1)
    return redirect('listfilm',request.user.username)
    
@login_required
def DelFilm(request,id):
    UserListF.objects.filter(film_id=id,user=request.user.id).delete()
    return redirect('listfilm',request.user.username)

@login_required
def userlist(request,username):
    if not username:
        user=request.user
    else:
        user=User.objects.get(username=username)
    lists={}
    
    if request.GET.get('groups'):
        for i in request.GET.get('groups').split(' '):
            status=UserStat.get(i)
            if status:
                lists.update({
                    i:{
                        "name":status['name'],
                        "list":getFilmlist(user.id,status['id']),
                    }
                })
    else:
        for i in UserStat.items():
            lists.update({
                i[0]:{
                    "name":i[1]['name'],
                    "list":getFilmlist(user.id,i[1]['id']),
                }
            })
            
    return render(request,"List/list.html",{
        "groups":lists,
        "type":"films",
    })

def getFilmlist(userid,statusid):
    return UserListF.objects.filter(user_id=userid,userstatus=statusid).order_by("film__name")