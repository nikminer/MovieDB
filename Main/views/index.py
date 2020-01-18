from django.shortcuts import render,redirect
from Profile.models import Profile,Friendlist
from Main.models import Film,Serial
from django.db.models import Q

from List.views.feed import getFeed

def index(request):
    data={
        "series":Serial.objects.order_by("-id")[:5],
        "films":Film.objects.order_by("-id")[:5]
    }

    if request.user.is_authenticated:
        profile=Profile.objects.get(user__username=request.user.username)
        data.update({"profile":profile})
        myfriends=Friendlist.objects.filter(Q(accepter=profile) | Q(sender=profile))
        data.update({"friends":{
                "friends":myfriends.filter(status=1).count(),
                "requests":myfriends.filter(status=0).count() 
            }
        })

        feed=[profile]
        for freind in myfriends.filter(status=1):
            freindprofile=freind.getnotMyprofile(profile)
            if freindprofile:
                feed.append(freindprofile)

        data.update({"feed":getFeed(feed)})

    return render(request,"Main/index.html",data)
