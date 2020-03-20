from django.http import JsonResponse
from MyWatchList.models import WatchList
from django.contrib.auth.decorators import login_required
from List.views.feed import sendFeed, typeFeed
from django.views.decorators.http import require_POST
from Main.views.decoratiors import ajax_required

UserStat={
    "planned": 1,
    "watch": 2,
    "watched": 3,
    "rewatch": 4,
    "drop": 5
}

@ajax_required
@login_required
@require_POST
def incepisode(request):
    item = WatchList.objects.get(id=int(request.POST['listid']), user=request.user.id)
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

@ajax_required
@login_required
@require_POST
def decepisode(request):
    item = WatchList.objects.get(id=int(request.POST['listid']), user=request.user.id)
    
    if item.userepisode-1 >= 0:
        item.userepisode -= 1
        item.save()
        #sendFeed(item, typeFeed['dec'])
        return JsonResponse({'status': 'dec', "userepisode": item.userepisode})

    else:
        return JsonResponse({'status': 'false', "userepisode": item.userepisode})

@ajax_required
@login_required
@require_POST
def setepisode(request):
    item = WatchList.objects.get(id=int(request.POST['listid']), user=request.user.id)
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

@ajax_required
@login_required
@require_POST
def increwatched(request):
    item = WatchList.objects.get(id=int(request.POST['listid']), user=request.user.id)
    item.rewatch += 1
    item.save()
    return JsonResponse({'status': 'inc', "countreview": item.rewatch})

@ajax_required
@login_required
@require_POST
def decrewatched(request):
    item = WatchList.objects.get(id=int(request.POST['listid']), user=request.user.id)

    if item.rewatch - 1 >= 0:
        item.rewatch -= 1
        item.save()
        return JsonResponse({'status': 'inc', "countreview": item.rewatch})

    else:
        return JsonResponse({'status': 'false', "countreview": item.rewatch})

@ajax_required
@login_required
@require_POST
def setrewatched(request):
    item = WatchList.objects.get(id=int(request.POST['listid']), user=request.user.id)
    ep = int(request.POST['count'])
    if not ep < 0:
        item.rewatch = ep
        item.save()
        return JsonResponse({'status': 'inc', "countreview": item.rewatch})
    else:
        return JsonResponse({'status': 'false', "countreview": item.rewatch})