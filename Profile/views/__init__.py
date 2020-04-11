from . import auth, settings, messages, notifications, feed, followers

from django.shortcuts import render, get_object_or_404
from Profile.models import Profile, Follower
from django.db.models import Q

from Profile.views.feed import getFeed


def profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    data = {
        "profile": profile,
        "feed": getFeed(request, profile),
    }

    if profile.user != request.user and request.user.is_authenticated:
        data.update({"ifollow": Follower.objects.filter(follow_from=request.user.profile, follow_to=profile).exists()})

    return render(request, 'Profile/profile.html', data)

