from django.http import JsonResponse
from Main.models import UserList
from List.models import UserFeed
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

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
    item=UserList.objects.get(id=int(data['listid']),user=request.user.id)
    rating=int(data['rating'])
    if rating != item.userrate:
        if rating>=0 and rating<=10:
            item.userrate=rating
        elif rating<0:
            item.userrate=0
        elif rating>10:
            item.userrate=10
        item.save()
        
        item.season.rating=round(UserList.objects.filter(season_id=item.season_id).filter(userrate__gt=0).aggregate(Avg('userrate'))['userrate__avg'],2)
        item.season.save()

        feeditem=UserFeed.objects.filter(userlist__user=item.user,typeAction="rating").order_by("created").last()
        if feeditem and feeditem.userlist==item and feeditem.is_lasthour:
            feeditem.action="Оценил на {}".format(item.userrate)
            feeditem.save()
        else:
            UserFeed.objects.create(userlist=item,action="Оценил на {}".format(item.userrate),typeAction="rating")

    return JsonResponse({'status':'voted',"userrating":item.userrate})



@login_required
def setstatus(request):
    data=request.POST
    if data['listid']!="undefined":
        item=UserList.objects.get(id=int(data['listid']),user=request.user.id)
        if UserStat.get(data['status']) and item.userstatus!=UserStat.get(data['status']):
            item.userstatus=UserStat[data['status']]
            item.save()

            feeditem=UserFeed.objects.filter(userlist__user=item.user,typeAction="status").order_by("created").last()
            action = "Изменил статус на {}".format(UserStatus.get(data['status'])['name'])
            if feeditem and feeditem.userlist==item:
                feeditem.action="Изменил статус на {}".format(UserStatus.get(data['status'])['name'])
                feeditem.lastaction 
                feeditem.save()
            else:
                UserFeed.objects.create(userlist=item,action="Изменил статус на {}".format(UserStatus.get(data['status'])['name']),typeAction="status")

            return JsonResponse({'status':'changestatus','userstatus':data['status']})
    return JsonResponse({'status':'false'})