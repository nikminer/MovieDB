from django.shortcuts import render,redirect
from Profile.models import Profile,Friendlist
from django.db.models import Q

def index(request):
    data={}
    if request.is_authenticated:
        profile=Profile.objects.get(user__username=request.user.username)
        data.update({"profile":profile})
        myfriends=Friendlist.objects.filter(Q(accepter=profile) | Q(sender=profile))
        data.update({"friends":{
                "friends":myfriends.filter(status=1).count(),
                "requests":myfriends.filter(status=0).count()  
            }
        })
    return render(request,"Main/index.html",data)
