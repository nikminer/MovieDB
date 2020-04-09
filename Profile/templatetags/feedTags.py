from django import template
from Profile.views.feed import getFeed


register = template.Library()


@register.inclusion_tag("Profile/blocks/Feed_activity_ajax.html", takes_context=True)
def FeedActivity(context):
    profile= context['user'].profile
    return {
        'profile': profile,
        'feed': getFeed(context['request'], profile, followers=True),
    }
