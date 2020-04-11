from django.shortcuts import render, get_object_or_404
from Profile.models import Notifications
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def notifications(request):
    data = {
        "notifications": Notifications.objects.filter(profile=request.user.profile).order_by("sended")
    }

    return render(request, 'Profile/notifications.html', data)


@login_required
def deletenotification(request):
    if request.POST['id']:
        noti = get_object_or_404(Notifications, id=request.POST['id'])
        if noti.profile == request.user.profile:
            noti.delete()
            return JsonResponse({"resp": True})
    return JsonResponse({"resp": False})


def addnotification(message, profile, obj=None):
    noti = Notifications.objects.create(profile=profile, message=message)

    if obj:
        noti.item = obj
    noti.save()
    return True
