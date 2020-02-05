from django import template
from Main.models import UserList,UserListF,Film,Serial
from Profile.models import Friendlist
from django.db.models import Q

register = template.Library()

@register.inclusion_tag("Main/blocks/friends.html")
def friends(profile):

    myfriends = Friendlist.objects.filter(Q(accepter=profile) | Q(sender=profile))
    return {
        'friends':{
                "friends":myfriends.filter(status=1).count(),
                "requests":myfriends.filter(status=0).count()
            },
        'profile':profile,
    }

@register.inclusion_tag("Main/blocks/MyLastFilms.html")
def MyLastFilms(profile):

    return {
        "films":Film.objects.filter(id__in=UserListF.objects.filter(user=profile.user).order_by('-updated').values_list("film",flat=True)[:5]),
        "username":profile.user.username
    }

@register.inclusion_tag("Main/blocks/MyLastSerials.html")
def MyLastSeries(profile):
    serials=[]
    for i in UserList.objects.filter(user=profile.user).order_by('-updated').values_list("serial",flat=True):
        if i not in serials:
            serials.append(i)
            if len(serials)>=5:
                break
    return {
        "series":Serial.objects.filter(id__in=serials),
        "username":profile.user.username
    }