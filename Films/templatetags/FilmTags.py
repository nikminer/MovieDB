from django import template

from Main.models import UserListF
from Profile.models import Friendlist

register = template.Library()

@register.inclusion_tag("Films/blocks/Friends.html")
def friendListF(profile,film):
    return {
        'friends': UserListF.objects.filter(
            user__in=Friendlist.friends.get_friends(profile),
            film=film
        ).order_by('user__first_name')
    }
