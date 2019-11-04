from django.shortcuts import render,redirect
from Profile.models import Profile,Friendlist
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

@login_required
def Friends(request,username):
    profile=Profile.objects.get(user__username=username)
    friendlist=[]
    myfriends=Friendlist.objects.filter(Q(accepter=profile) | Q(sender=profile))

    for i in myfriends.filter(status=1).order_by("-id"):
        if i.accepter==profile:
            friendlist.append(i.sender)
        else:
            friendlist.append(i.accepter)
    
    data={
        "profile":profile,
        "friends":{
            "list":friendlist,
            "count":myfriends.filter(status=1).count(),
            "requestcount":myfriends.filter(accepter=profile,status=0).count()
        },
    }
    return render(request, 'Profile/friends.html',data)

@login_required
def Friendsreq(request,username):
    profile=Profile.objects.get(user__username=username)
    if profile.user!=request.user:
        return redirect("friendreq",request.user.username)
    else:
        friendlist=[]
        myfriends=Friendlist.objects.filter(accepter=profile)
        for i in myfriends.filter(status=0).order_by("-id"):
            i.sender.idlink=i.id
            friendlist.append(i.sender)
        friendlist2=[]
        myfriends2=Friendlist.objects.filter(sender=profile)
        for i in myfriends2.filter(status=0).order_by("-id"):
            i.accepter.idlink=i.id
            friendlist2.append(i.accepter)

        data={
            "profile":profile,
            "friends":{
                "list":friendlist,
                "count":myfriends.filter(accepter=profile,status=0).count(),
                "list2":friendlist2,
                "count2":myfriends2.filter(sender=profile,status=0).count(),
                "fcount":myfriends.filter(status=1).count(),
            },
        }

        return render(request, 'Profile/friendsreq.html',data)

@login_required
def addfriend(request,username):
    if username != request.user.username:
        profile1=Profile.objects.get(user=request.user)
        profile2=Profile.objects.get(user__username=username)
        if Friendlist.objects.filter(Q(accepter=profile1, sender=profile2) | Q(sender=profile1, accepter=profile2)).count()==0:
            Friendlist.objects.create(sender=profile1,accepter=profile2)
            messages.success(request, "Запрос дружбы успешно отправлен!")
    else:
        messages.error(request, 'Нельзя отправить самому себе запрос дружбы!')
    return redirect('profile',username)

@login_required
def Removefriend(request,username):
    if username != request.user.username:
        profile=Profile.objects.get(user__username=username)
        myprofile=Profile.objects.get(user=request.user)
        friendlink=Friendlist.objects.filter(Q(Q(accepter=myprofile) & Q(sender=profile)) | Q(Q(sender=myprofile)& Q(accepter=profile))).filter(status=1)
        if friendlink.count()!=0:
            friendlink.delete()
            messages.success(request,'Пользователь {} {} был убран из ваших друзей'.format(profile.user.first_name,profile.user.last_name))
    else:
        messages.error(request, 'Нельзя удалить себя из ваших друзей!')
    return redirect("profile",username)

@login_required
def Acceptfriend(request,id,username):
    friendlink=Friendlist.objects.get(id=id)
    if friendlink.accepter.user==request.user and friendlink.status==0:
        friendlink.status=1
        friendlink.save()
    return redirect("friendreq",username)

@login_required
def Declinefriend(request,id,username):
    friendlink=Friendlist.objects.get(id=id)
    profile=Profile.objects.get(user__username=username)
    if (friendlink.accepter.user==request.user or friendlink.sender.user==request.user) and profile.user==request.user:
        friendlink.delete()
    return redirect("friendreq",username)