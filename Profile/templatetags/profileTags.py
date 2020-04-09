from django import template
from ..models import Follower


register = template.Library()

@register.inclusion_tag("Profile/tags/UsersSection.html")
def Myfollowers(profile):
    followers = profile.followers.all()
    return {
        'profile': profile,
        'items': followers[:5],
        'count': followers.count(),
        'urlname': 'followers',
        'sectionname': "Подписчики"
    }


@register.inclusion_tag("Profile/tags/UsersSection.html")
def Myfollowings(profile):
    following = profile.following.all()
    return {
        'profile': profile,
        'items': following[:10],
        'count': following.count(),
        'urlname': 'followings',
        'sectionname': "Подписки"
    }
