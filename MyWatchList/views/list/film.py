from django.shortcuts import render,redirect
from Main.models import UserListF,Film
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 

from List.views.userstatus import UserStat

from MyWatchList.models import Movie, WatchList


'''
@login_required
def AddFilm(request,id):
    UserListF.objects.create(user_id=request.user.id,film_id=id,userstatus=1)
    return redirect('listfilm',request.user.username)
    
@login_required
def DelFilm(request,id):
    UserListF.objects.filter(film_id=id,user=request.user.id).delete()
    return redirect('listfilm',request.user.username)
'''