from . import film,series,list

from . import addmovie, decoratiors, ErrorsHandler


from django.shortcuts import render
from Profile.models import Friendlist
from django.db.models import Q

def index(request):


    if request.user.is_authenticated:
        profile=request.user.profile
        myfriends=Friendlist.objects.filter(Q(accepter=profile) | Q(sender=profile))

    return render(request, "Main/index.html")
