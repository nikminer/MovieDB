from django.http import JsonResponse
from Main.models import UserListS
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from List.views.feed import sendFeed,typeFeed
from List.views.userstatus import UserStat as UserStatus

UserStat={
    "planned":1,
    "watch":2,
    "watched":3,
    "rewatch":4,
    "drop":5
}


@login_required
def setrating(request):

    data=request.POST
    item=UserListS.objects.get(id=int(data['listid']),user=request.user)
    rating=int(data['rating'])
    if rating != item.userrate:
        if rating>=0 and rating<=10:
            item.userrate=rating
        elif rating<0:
            item.userrate=0
        elif rating>10:
            item.userrate=10
        item.save()
        
        item.season.rating=round(UserListS.objects.filter(season_id=item.season_id).filter(userrate__gt=0).aggregate(Avg('userrate'))['userrate__avg'],2)
        item.season.save()

        sendFeed(item,typeFeed['rating'])

    return JsonResponse({'status':'voted',"userrating":item.userrate})



@login_required
def setstatus(request):
    data=request.POST
    if data['listid']!="undefined":
        item=UserListS.objects.get(id=int(data['listid']),user=request.user.id)
        if UserStat.get(data['status']) and item.userstatus!=UserStat.get(data['status']):
            item.userstatus=UserStat[data['status']]
            item.save()

            sendFeed(item,typeFeed['status'])

            return JsonResponse({'status':'changestatus','userstatus':data['status']})
    return JsonResponse({'status':'false'})



    