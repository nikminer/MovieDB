from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from Main.models import Film,GenreF,UserListF
from django.contrib.auth.decorators import login_required
from List.views.feed import sendFeed,typeFeed

def film(request,id):
    film=get_object_or_404(Film,id=id)
        
    data={
        "Film":film,
    }
    
    try:
        data.update({"UserItem":UserListF.objects.get(film_id=id,user=request.user.id)})
    except UserListF.DoesNotExist:
        pass
        
    return render(request,"Films/film.html",data)



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
    item=UserListF.objects.get(id=int(data['listid']),user=request.user.id)
    rating=int(data['rating'])
    if rating>=0 and rating<=10:
        item.userrate=rating
    elif rating<0:
        item.userrate=0
    elif rating>10:
        item.userrate=10
    item.save()
    
    sendFeed(item,typeFeed['rating'])

    item.film.rating=round(UserListF.objects.filter(film_id=item.film_id).filter(userrate__gt=0).aggregate(Avg('userrate'))['userrate__avg'],2)
    item.film.save()
    
    return JsonResponse({'status':'voted',"userrating":item.userrate})

@login_required
def setstatus(request):
    if request.POST:
        data=request.POST
        if data['listid']!="undefined":
            item=UserListF.objects.get(id=int(data['listid']),user=request.user.id)
            if UserStat.get(data['status']):
                item.userstatus=UserStat[data['status']]
                item.save()

                sendFeed(item,typeFeed['status'])

                return JsonResponse({'status':'changestatus','userstatus':data['status']})
        else:
            return JsonResponse({'status':'false'})
    else:
        return JsonResponse({'status':'false'})