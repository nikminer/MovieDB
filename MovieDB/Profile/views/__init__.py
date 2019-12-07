from . import friends,auth,settings,messages,notifications


from django.shortcuts import render,get_object_or_404
from Profile.models import Profile,Friendlist
from django.contrib.auth.decorators import login_required
from Main.models import UserList,UserListF
from django.db.models import Q

from List.views.feed import getFeed

def profile(request,username):
    profile=get_object_or_404(Profile,user__username=username)
    friendlist=[]
    myfriends=Friendlist.objects.filter(Q(accepter=profile) | Q(sender=profile))
    for i in myfriends.filter(status=1).order_by("-id")[0:10]:
        if i.accepter==profile:
            friendlist.append(i.sender)
        else:
            friendlist.append(i.accepter)
    
    data={
        "profile":profile,
        "serials":Movie(UserList,profile.user.id),
        "films":Movie(UserListF,profile.user.id),
        "friends":{
            "list":friendlist,
            "count":len(myfriends.filter(status=1)),
            "requestcount":myfriends.filter(accepter=profile,status=0).count()
        },
        "feed":getFeed([profile]),
    }

    if profile.user != request.user and request.user.is_authenticated:
        myprofile = Profile.objects.get(user=request.user)
        myfriends = Friendlist.objects.filter(Q(Q(accepter=myprofile) & Q(sender=profile)) | Q(Q(sender=myprofile)& Q(accepter=profile))).filter(status=1)
        if myfriends.count()==0:
            data.update({
                "ismyfriend":False
            })
        else:
            data.update({
                "ismyfriend":True
            })
    return render(request, 'Profile/profile.html',data)


class Movie:
    watched=None
    planned=None
    watch=None
    def __init__(self,dbobj,id):
        planned=len(dbobj.objects.filter(Q(user_id=id) & Q(userstatus=1)))
        watch=len(UserList.objects.filter(Q(user_id=id) & (Q(userstatus=2)|Q(userstatus=4))))
        watched=len(dbobj.objects.filter(Q(user_id=id) & Q(userstatus=3)))
        try:
            one=100/(planned+watch+watched)
        except ZeroDivisionError:
            one=100
        self.watch=MovieElem(watch,one*watch)   
        self.planned=MovieElem(planned,one*planned)
        self.watched=MovieElem(watched,one*watched)
        del one,planned,watch,watched

class MovieElem:
    count=0
    width=""
    def __init__(self,count,width):
        self.count=count
        self.width=str(width).replace(",",".")