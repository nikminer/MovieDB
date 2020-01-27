from django.shortcuts import render,redirect
from Main.models import UserList,Season,Serial
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.db.models import Count
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
    for i in UserList.objects.filter(user_id=user.id).only('serial').values_list('serial', flat=True).distinct():
        for tag in Serial.objects.get(id=i).tags.all():
            if genrelist.get(tag.name):
                genrelist[tag.name]['count'] += 1
            else:
                genrelist.update({tag.name: {'count': 1, 'tag': tag.slug}})

    genrelist = dict(sorted(genrelist.items()))


    return render(request,"List/list.html",{
        "groups":lists,
        "type":"series",
        "user":user,
        "genrelist": genrelist,
    })


def getSeriallist(userid,statusid,request):
    serialDict={}
    userl=UserList.objects.filter(user_id=userid,userstatus=statusid).order_by("serial__name")

    if request.GET.get('genres'):
        userl= userl.filter(serial__tags__slug__in=request.GET.get('genres').split(' '))

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
    item.width= str(int(100/item.episodes*item.watched))+"%"
class SerialItem:
    serial=None
    seasons=[]
    episodes=0
    watched=0
    width="0%"
    def __init__(self):
        self.serial=None
        self.seasons=[]