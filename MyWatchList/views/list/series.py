from django.shortcuts import render,redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.db.models import Count
from List.views.userstatus import UserStat

from MyWatchList.models import WatchList,Movie,Season




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