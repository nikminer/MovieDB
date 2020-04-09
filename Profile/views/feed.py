import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from ..models import Feed, Profile
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from MyWatchList.views.decoratiors import ajax_required
from django.contrib.auth.decorators import login_required

def create_feed(profile, verb):
    last_minute = timezone.now() - datetime.timedelta(seconds=60)
    similar_actions = Feed.objects.filter(profile=profile, verb=verb,
                                          created__gte=last_minute)

    if not similar_actions:
        action = Feed(profile=profile, verb=verb)
        action.save()
        return True
    return False

def create_item_feed(profile, verb, item, itemType):
    last_hours = timezone.now() - datetime.timedelta(hours=3)
    item_ct = ContentType.objects.get_for_model(item)
    try:
        action = Feed.objects.get(
            profile=profile,
            created__gte=last_hours,
            feed_type=itemType,
            item_ct=item_ct,
            item_id=item.id
        )
        action.verb=verb
        action.save()
        return False
    except Feed.DoesNotExist:
        Feed.objects.create(profile=profile, verb=verb, item=item, feed_type=itemType)
        return True


def getFeed(request, profile, page=1, followers=False):
    if followers:
        feed = Feed.objects.filter(Q(profile__in=profile.following.all()) | Q(profile=profile))
    else:
        feed = Feed.objects.filter(profile=profile)

    feed.order_by("-created")

    paginator = Paginator(feed, 25)

    try:
        feed = paginator.page(page)
    except PageNotAnInteger:
        feed = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse(None)
        feed = paginator.page(paginator.num_pages)

    return feed


@ajax_required
def Profileactivity(request, username, page):
    profile = get_object_or_404(Profile, user__username=username)

    data = {
        "feed": getFeed(request, profile, page=page),
        "profile": profile,
    }

    return render(request, "Profile/blocks/Profile_feed_ajax.html", data)

@login_required
@ajax_required
def Indexactivity(request, username, page):
    profile = get_object_or_404(Profile, user__username=username)
    data = {
        "feed": getFeed(request, profile, followers=True, page=page),
        "profile": profile,
    }

    return render(request, "Profile/blocks/Feed_activity_ajax.html", data)
