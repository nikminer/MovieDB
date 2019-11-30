from django.http import JsonResponse
from Main.models import UserList,Season
from django.contrib.auth.decorators import login_required
from List.views.feed import sendFeed,typeFeed

UserStat={
    "planned":1,
    "watch":2,
    "watched":3,
    "rewatch":4,
    "drop":5
}

@login_required
def incepisode(request):
    data=request.POST
    item=UserList.objects.get(id=int(data['listid']),user=request.user.id)
    if item.userepisode+1<item.season.episodecount:
        item.userepisode+=1
        '''if item.userstatus==UserStat['planned']:
            item.userstatus=UserStat['watch']
        elif item.userstatus==UserStat['watched']:
            item.userstatus=UserStat['rewatch']
        '''
        sendFeed(item,typeFeed['inc'])
        item.save()
        return JsonResponse({'status':'inc',"userepisode":item.userepisode})
    elif item.userepisode+1==item.season.episodecount:
        item.userepisode+=1
        item.userstatus=UserStat['watched']
        sendFeed(item,typeFeed['status'])
        item.save()
        return JsonResponse({'status':'watched',"userepisode":item.userepisode})
    else:
        return JsonResponse({'status':'false',"userepisode":item.userepisode})
        
@login_required
def decepisode(request):
    data=request.POST
    item=UserList.objects.get(id=int(data['listid']),user=request.user.id)
    
    if item.userepisode-1>=0:
        item.userepisode-=1
        item.save()
        return JsonResponse({'status':'dec',"userepisode":item.userepisode})
    else:
        return JsonResponse({'status':'false',"userepisode":item.userepisode})

@login_required
def setepisode(request):
    data=request.POST
    item=UserList.objects.get(id=int(data['listid']),user=request.user.id)
    ep=int(data['count'])
    if not ep < 0 and not ep > item.season.episodecount:
        item.userepisode=ep
        item.save()
        return JsonResponse({'status':'set',"userepisode":item.userepisode})
    else:
        return JsonResponse({'status':'false',"userepisode":item.userepisode})