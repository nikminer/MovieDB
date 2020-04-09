from . import auth,settings,messages,notifications,feed,followers

from django.shortcuts import render,get_object_or_404
from Profile.models import Profile,Follower
from Main.models import UserList,UserListF
from django.db.models import Q

from Profile.views.feed import getFeed

def profile(request,username):
    profile=get_object_or_404(Profile,user__username=username)
    
    data={
        "profile":profile,
        "serials":Movie(UserList, profile.user.id),
        "films":Movie(UserListF, profile.user.id),
        "feed":getFeed(request, profile),
    }

    if profile.user != request.user and request.user.is_authenticated:
        data.update({"ifollow": Follower.objects.filter(follow_from=request.user.profile, follow_to=profile).exists()})

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