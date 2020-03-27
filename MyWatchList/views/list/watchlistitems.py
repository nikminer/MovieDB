from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from List.views.feed import sendFeed, typeFeed
from MyWatchList.models import WatchList
from django.db.models import Avg
from django.views.decorators.http import require_POST
from Main.views.decoratiors import ajax_required
from .userstatus import UserStat


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

@ajax_required
@login_required
@require_POST
def rewatch(request):
    data = request.POST

    if data['status'] == 'inc':
        item = WatchList.objects.get(id=int(data['listid']), user=request.user.id)
        item.rewatch += 1
        item.save()
        return JsonResponse({'status': True, "countreview": item.rewatch})

    elif data['status'] == 'dec':
        item = WatchList.objects.get(id=int(data['listid']), user=request.user.id)
        if item.rewatch - 1 >= 0:
            item.rewatch -= 1
            item.save()
            return JsonResponse({'status': True, "countreview": item.rewatch})
        else:
            return JsonResponse({'status': False, "countreview": item.rewatch})

    elif data['status'] == 'set':
        item = WatchList.objects.get(id=int(data['listid']), user=request.user.id)
        ep = int(data['count'])
        if not ep < 0:
            item.rewatch = ep
            item.save()
            return JsonResponse({'status': True, "countreview": item.rewatch})
        else:
            return JsonResponse({'status': False, "countreview": item.rewatch})








@ajax_required
@login_required
@require_POST
def setstatus(request):
    data = request.POST
    if data['listid'] != "undefined":
        item = WatchList.objects.get(id=int(data['listid']), user=request.user.id)
        if UserStat.get(data['status']):
            item.userstatus = UserStat[data['status']]
            item.save()

            sendFeed(item, typeFeed['status'])

            return JsonResponse({'status': 'changestatus', 'userstatus': data['status']})

    return JsonResponse({'status': 'false'})