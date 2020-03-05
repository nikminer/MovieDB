from django.http import JsonResponse
from Main.models import UserList
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

        sendFeed(item,typeFeed['rating'])

    return JsonResponse({'status':'voted',"userrating":item.userrate})



@login_required
def setstatus(request):
    data = request.POST
    Datarequest = {'status':'false'}

    if data['listid']!="undefined":

        for itemid in str(data['listid']).split(";"):
            item=UserList.objects.get(id=int(itemid),user=request.user.id)

            if UserStat.get(data['status']) and item.userstatus!=UserStat.get(data['status']):
                if item.userstatus == UserStat['rewatch'] and UserStat.get(data['status']) == UserStat['watched']:
                    item.countreview+=1

                if item.userstatus in (UserStat['planned'], UserStat['watch'], UserStat['rewatch']) and UserStat.get(data['status']) == UserStat['watched']:
                    item.userepisode = item.season.episodecount

                if item.userstatus == UserStat['watched'] and UserStat.get(data['status']) in (UserStat['planned'], UserStat['watch'], UserStat['rewatch']):
                    item.userepisode=0;

                item.userstatus=UserStat[data['status']]
                item.save()

                sendFeed(item,typeFeed['status'])
                Datarequest={'status': 'changestatus', 'userstatus': data['status'], 'userepisode': item.userepisode}


        return JsonResponse(Datarequest)

    return JsonResponse(Datarequest)
