from django.shortcuts import render,redirect,get_object_or_404
from Profile.models import Profile,Notifications
from django.contrib.auth.decorators import login_required
from Main.models import Film,Serial
from django.db.models import Q
from django.http import JsonResponse


@login_required
def notifications(request):
    data={
        "notifications": Notifications.objects.filter(profile=request.user.profile).order_by("sended")
    }

    return render(request, 'Profile/notifications.html',data)



@login_required
def deletenotification(request):
    if request.POST['id']:
        noti= get_object_or_404(Notifications,id=request.POST['id'])
        if noti.profile == request.user.profile:
            noti.delete()
            return JsonResponse({"resp":True})
    return JsonResponse({"resp":False})



def addnotification(message,obj,profile):
    noti=Notifications.objects.create(profile=profile,message=message)
    if type(obj)is Serial:
        noti.serial = obj
        noti.save()
        return True
    elif type(obj) is Film:
        noti.film = obj
        noti.save()
        return True
    else:
        print(type(obj))
        noti.delete()
    return False