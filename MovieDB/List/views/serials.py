from django.shortcuts import render,redirect
from Main.models import UserList,Season
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 

from List.views.userstatus import UserStat

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
    
    lists={}
    
    if request.GET.get('groups'):
        for i in request.GET.get('groups').split(' '):
            status=UserStat.get(i)
            if status:
                lists.update({
                    i:{
                        "name":status['name'],
                        "list":getSeriallist(user.id,status['id']),
                    }
                })
    else:
        for i in UserStat.items():
            lists.update({
                i[0]:{
                    "name":i[1]['name'],
                    "list":getSeriallist(user.id,i[1]['id']),
                }
            })
    
    return render(request,"List/nlist.html",{
        "groups":lists,
        "type":"series"
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