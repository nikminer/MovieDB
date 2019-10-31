from django.shortcuts import render,redirect
from Main.models import UserListF
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 

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
    
    user=User.objects.get(username=username)
    return render(request,"List/listf.html",{
        "planlist":getFilmlist(user.id,1),
        "watchlist":getFilmlist(user.id,2),
        "watchedlist":getFilmlist(user.id,3),
        "reviewlist":getFilmlist(user.id,4),
        "droplist":getFilmlist(user.id,5),
    })

def getFilmlist(userid,statusid):
    return UserListF.objects.filter(user_id=userid,userstatus=statusid)