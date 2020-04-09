import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from ..models import Feed
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def create_feed(profile, verb, item=None):
    last_minute = timezone.now() - datetime.timedelta(seconds=60)
    similar_actions = Feed.objects.filter(profile=profile, verb=verb,
                                          created__gte=last_minute)
    if item:
        item_ct = ContentType.objects.get_for_model(item)
        similar_actions = similar_actions.filter(item_ct=item_ct,
                                                 item_id=item.id)
    if not similar_actions:
        action = Feed(profile=profile, verb=verb, item=item)
        action.save()
        return True
    return False


def getFeed(request, profile, page=1, followers=False):

    if followers:
        feed = Feed.objects.filter(Q(profile__in=profile.following.all()) | Q(profile=profile))
    else:
        feed = Feed.objects.filter(profile=profile)

    feed.order_by("-created")

    paginator = Paginator(feed, 5)

    try:
        feed = paginator.page(page)
    except PageNotAnInteger:
        feed = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse(None)
        feed = paginator.page(paginator.num_pages)

    return feed

def ProfileActivity(request,page=1):

    Serials=Movie.manager.get_series().order_by("-year", "name")

    if request.is_ajax():
        return render(request, "Serials/blocks/List_Ajax.html", {
            'urlname': 'seriallist_page',
            'items': ListFeature(request, page, Serials)
        })
    else:
        return render(request, "Serials/seriallist.html", {
            "SerialList": ListFeature(request, page, Serials),
        })