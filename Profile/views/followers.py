from django.shortcuts import render,redirect,get_object_or_404
from Profile.models import Profile, Follower
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages


@login_required
def followers(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    followers = profile.followers.all().order_by("-id")

    data = {
        "profile": profile,
        "followers": followers,
        "count": followers.count(),
        "followingcount": profile.following.all().count()
    }
    return render(request, 'Profile/followers.html', data)

@login_required
def following(request,username):
    profile=get_object_or_404(Profile,user__username=username)

    following = profile.following.all().order_by("-id")

    data = {
        "profile": profile,
        "followers": following,
        "count": following.count(),
        "followersgcount": profile.followers.all().count()
    }
    return render(request, 'Profile/following.html', data)

@login_required
def follow(request, username):
    if username != request.user.username:
        to_profile=Profile.objects.get(user__username=username)
        from_profile = request.user.profile
        try:
            Follower.objects.get(follow_from=from_profile, follow_to=to_profile).delete()
            messages.success(request, "Вы успешно отписались от {}!".format(to_profile.name))
        except Follower.DoesNotExist:
            Follower.objects.create(follow_from=from_profile, follow_to=to_profile)
            messages.success(request, "Вы успешно подписались на {}!".format(to_profile.name))

    return redirect('profile', username)