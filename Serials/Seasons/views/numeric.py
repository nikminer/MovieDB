from django.http import JsonResponse
from Main.models import UserList, Season
from django.contrib.auth.decorators import login_required
from List.views.feed import sendFeed, typeFeed

UserStat={
    "planned": 1,
    "watch": 2,
    "watched": 3,
    "rewatch": 4,
    "drop": 5
}

@login_required
def incepisode(request):
    item = UserList.objects.get(id=int(request.POST['listid']), user=request.user.id)
    if item.userepisode+1 < item.season.episodecount:
        item.userepisode += 1
        if item.userstatus == UserStat['planned']:
            item.userstatus = UserStat['watch']

        sendFeed(item, typeFeed['inc'])
        item.save()
        return JsonResponse({'status': 'inc', "userepisode": item.userepisode})

    elif item.userepisode+1 == item.season.episodecount:
        item.userepisode += 1
        item.userstatus = UserStat['watched']
        sendFeed(item, typeFeed['status'])
        item.save()
        return JsonResponse({'status': 'watched', "userepisode": item.userepisode})

    else:
        return JsonResponse({'status': 'false', "userepisode": item.userepisode})
        
@login_required
def decepisode(request):
    item = UserList.objects.get(id=int(request.POST['listid']), user=request.user.id)
    
    if item.userepisode-1 >= 0:
        item.userepisode -= 1
        item.save()
        #sendFeed(item, typeFeed['dec'])
        return JsonResponse({'status': 'dec', "userepisode": item.userepisode})

    else:
        return JsonResponse({'status': 'false', "userepisode": item.userepisode})

@login_required
def setepisode(request):
    item = UserList.objects.get(id=int(request.POST['listid']), user=request.user.id)
    ep = int(request.POST['count'])
    if not ep < 0 and not ep > item.season.episodecount:
        item.userepisode = ep
        item.userstatus = UserStat['watched']
        item.save()
        return JsonResponse({'status': 'set', "userepisode": item.userepisode})

    elif ep > item.season.episodecount:
        item.userepisode = item.season.episodecount
        item.userstatus = UserStat['planned']
        item.save()
        return JsonResponse({'status': 'set', "userepisode": item.userepisode})

    else:
        return JsonResponse({'status': 'false', "userepisode": item.userepisode})

@login_required
def increwatched(request):
    item = UserList.objects.get(id=int(request.POST['listid']), user=request.user.id)
    item.countreview += 1
    item.save()
    return JsonResponse({'status': 'inc', "countreview": item.countreview})

@login_required
def decrewatched(request):
    item = UserList.objects.get(id=int(request.POST['listid']), user=request.user.id)

    if item.countreview - 1 >= 0:
        item.countreview -= 1
        item.save()
        return JsonResponse({'status': 'inc', "countreview": item.countreview})

    else:
        return JsonResponse({'status': 'false', "countreview": item.countreview})

@login_required
def setrewatched(request):
    item = UserList.objects.get(id=int(request.POST['listid']), user=request.user.id)
    ep = int(request.POST['count'])
    if not ep < 0:
        item.countreview  = ep
        item.save()
        return JsonResponse({'status': 'inc', "countreview": item.countreview})
    else:
        return JsonResponse({'status': 'false', "countreview": item.countreview})