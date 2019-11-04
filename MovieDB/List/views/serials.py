from django.shortcuts import render,redirect
from Main.models import UserList,Season
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 

@login_required
def AddSerial(request,id):
    seasons=[]
    for i in UserList.objects.filter(serial=id,user=request.user.id):
        seasons.append(i.season)
    for season in Season.objects.filter(serial=id):
        if not season in seasons:
            UserList.objects.create(user_id=request.user.id,season_id=season.id,serial_id=id,userstatus=1)
    return redirect('listserial',request.user.username)
    
@login_required
def DelSerial(request,id):
    UserList.objects.filter(serial=id,user=request.user.id).delete()
    return redirect('listserial',request.user.username)


@login_required
def userlist(request,username=None):
    if not username:
        user=request.user
    else:
        user=User.objects.get(username=username)
    return render(request,"List/list.html",{
        "planlist":getSeriallist(user.id,1),
        "watchlist":getSeriallist(user.id,2),
        "watchedlist":getSeriallist(user.id,3),
        "reviewlist":getSeriallist(user.id,4),
        "droplist":getSeriallist(user.id,5),
    })

def getSeriallist(userid,statusid):
    serialDict={}
    userl=UserList.objects.filter(user_id=userid,userstatus=statusid).order_by("serial__name")
    for i in userl:
        if not serialDict.get(i.serial.id):
            item=SerialItem()
            item.seasons.append(i)
            item.serial=i.serial
            getUserProgress(item,i.serial.id,userid)

            serialDict.update({i.season.serial.id:item})
        else:
            serialDict[i.season.serial.id].seasons.append(i)
    return serialDict.values()

def getUserProgress(item,serialid,userid):
    userl=UserList.objects.filter(user_id=userid,serial=serialid)
    item.episodes=0
    item.watched=0
    for i in userl:
            item.episodes+=i.season.episodecount
            item.watched+=i.userepisode

class SerialItem:
    serial=None
    seasons=[]
    episodes=0
    watched=0
    def __init__(self):
        self.serial=None
        self.seasons=[]