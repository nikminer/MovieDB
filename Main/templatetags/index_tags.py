from django import template
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
