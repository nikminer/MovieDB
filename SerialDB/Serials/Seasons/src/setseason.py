from django.http import JsonResponse
from Main.models import UserList
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

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
    item=UserList.objects.get(id=int(data['listid']),user=request.user.id)
    rating=int(data['rating'])
    if rating>=0 and rating<=10:
        item.userrate=rating
    elif rating<0:
        item.userrate=0
    elif rating>10:
        item.userrate=10
    item.save()

    item.season.rating=round(UserList.objects.filter(season_id=item.season_id).filter(userrate__gt=0).aggregate(Avg('userrate'))['userrate__avg'],2)
    item.season.save()
    
    return JsonResponse({'status':'voted',"userrating":item.userrate})

@login_required
def setstatus(request):
    data=request.POST
    if data['listid']!="undefined":
        item=UserList.objects.get(id=int(data['listid']),user=request.user.id)
        if UserStat.get(data['status']):
            item.userstatus=UserStat[data['status']]
            item.save()
            return JsonResponse({'status':'changestatus','userstatus':data['status']})
    return JsonResponse({'status':'false'})