from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from MyWatchList.models import WatchList
from django.db.models import Avg
from django.views.decorators.http import require_POST
from Main.views.decoratiors import ajax_required, listID_requeired
from .userstatus import UserStat

@listID_requeired
@ajax_required
@login_required
@require_POST
def setrating(request):
    data = request.POST

    item = WatchList.objects.get(id=int(data['listid']), user=request.user.id)
    rating = int(data['rating'])
    if rating >= 0 and rating <= 10:
        item.userrate = rating
    elif rating < 0:
        item.userrate = 0
    elif rating > 10:
        item.userrate = 10
    item.save()

    #sendFeed(item, typeFeed['rating'])

    if item.season:
        item.season.rating= round(
            WatchList.objects.filter(season=item.season, userrate__gt=0).aggregate(Avg('userrate'))['userrate__avg'], 2)
        item.season.save()

    item.movie.rating = round(
        WatchList.objects.filter(movie=item.movie, userrate__gt=0).aggregate(Avg('userrate'))['userrate__avg'], 2)
    item.movie.save()

    return JsonResponse({'status': 'voted', "userrating": item.userrate})

@listID_requeired
@ajax_required
@login_required
@require_POST
def rewatch(request):
    data = request.POST

    if data.get('status') == 'inc':
        item = WatchList.objects.get(id=int(data['listid']), user=request.user.id)
        if item.rewatch + 1 <= 255:
            item.rewatch += 1
            item.save()
            return JsonResponse({'status': True, "rewatch": item.rewatch})

    elif data.get('status') == 'dec':
        item = WatchList.objects.get(id=int(data['listid']), user=request.user.id)
        if item.rewatch - 1 >= 0:
            item.rewatch -= 1
            item.save()
            return JsonResponse({'status': True, "rewatch": item.rewatch})

    elif data.get('status') == 'set' and data.get('count'):
        item = WatchList.objects.get(id=int(data['listid']), user=request.user.id)
        ep = int(data['count'])
        if not ep < 0 and not ep > 255:
            item.rewatch = ep
            item.save()
        elif ep > 255:
            item.userepisode = 255
            item.userstatus = UserStat.get('planned')['id']
            item.save()
        return JsonResponse({'status': True, "rewatch": item.rewatch})

    return JsonResponse({'status': False})

@listID_requeired
@ajax_required
@login_required
@require_POST
def setepisode(request):
    data = request.POST

    if data.get('status') == 'inc':
        item = WatchList.objects.get(id=int(request.POST['listid']), user=request.user.id)
        if item.userepisode + 1 < item.season.episodecount:
            item.userepisode += 1
            if item.userstatus == UserStat.get('planned')['id']:
                item.userstatus = UserStat.get('watch')['id'];
            #sendFeed(item, typeFeed['inc'])
            item.save()
        elif item.userepisode + 1 == item.season.episodecount:
            item.userepisode += 1
            item.userstatus = UserStat.get('watched')['id']
            #sendFeed(item, typeFeed['status'])
            item.save()
        return JsonResponse({'status': True, "userepisode": item.userepisode})

    elif data.get('status') == 'dec':
        item = WatchList.objects.get(id=int(request.POST['listid']), user=request.user.id)
        if item.userepisode - 1 >= 0:
            item.userepisode -= 1
            item.save()
            # sendFeed(item, typeFeed['dec'])
        return JsonResponse({'status': True, "userepisode": item.userepisode})


    elif data.get('status') == 'set' and data.get('count'):
        item = WatchList.objects.get(id=int(request.POST['listid']), user=request.user.id)
        ep = int(request.POST['count'])
        if not ep < 0 and not ep > item.season.episodecount:
            item.userepisode = ep
            item.userstatus = UserStat.get('watched')['id']
            item.save()
        elif ep > item.season.episodecount:
            item.userepisode = item.season.episodecount
            item.userstatus = UserStat.get('planned')['id']
            item.save()
        return JsonResponse({'status': True, "userepisode": item.userepisode})

    return JsonResponse({'status': False})


@listID_requeired
@ajax_required
@login_required
@require_POST
def setstatus(request):
    data = request.POST
    item = WatchList.objects.get(id=int(data['listid']), user=request.user.id)
    if UserStat.get(data['status']):
        item.userstatus = UserStat.get(data['status'])['id']
        item.save()
        #sendFeed(item, typeFeed['status'])
        return JsonResponse({'status': True, 'userstatus': data['status']})
    return JsonResponse({'status': False})