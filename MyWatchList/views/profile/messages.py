from django.shortcuts import render,redirect,get_object_or_404
from MyWatchList.models import Profile,Messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse


@login_required
def Dialog(request,username):
    Sender = get_object_or_404(Profile,user=request.user)
    Accepter = get_object_or_404(Profile,user__username=username)
    messages= Messages.objects.get_dialog(Sender,Accepter)
    data={
        "Accepter":Accepter,
        "Sender":Sender,
        "Dialogmessages":messages,
    }

    return render(request, 'Profile/messages/dialog.html',data)

@login_required
def SendMessage(request,username):
    Sender = get_object_or_404(Profile,user=request.user)
    Accepter = get_object_or_404(Profile,user__username=username)
    if request.POST['message'] and len(request.POST['message'])>0:
        Messages.objects.create(FromUser=Sender,ToUser=Accepter,message=request.POST['message'])
        return JsonResponse({'status':'sended'})
    
    return JsonResponse({'status':None})

    
