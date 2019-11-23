from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from Main.models import Film,Genre,UserListF
from django.contrib.auth.decorators import login_required
from List.views.feed import sendFeed,typeFeed

def film(request,id):
    film=get_object_or_404(Film,movie=id)
        
    data={
        "Film":film,
    }
    
    try:
        data.update({"UserItem":UserListF.objects.get(movie=film.movie,user=request.user)})
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
    item=UserListF.objects.get(id=int(data['listid']),user=request.user)
    rating=int(data['rating'])
    if rating>=0 and rating<=10:
        item.userrate=rating
    elif rating<0:
        item.userrate=0
    elif rating>10:
        item.userrate=10
    item.save()
    
    sendFeed(item,typeFeed['rating'])
    film= Film.objects.get(movie=item.movie)
    film.rating=round(UserListF.objects.filter(movie=item.movie).filter(userrate__gt=0).aggregate(Avg('userrate'))['userrate__avg'],2)
    film.save()
    
    return JsonResponse({'status':'voted',"userrating":item.userrate})

@login_required
def setstatus(request):
    if request.POST:
        data=request.POST
        if data['listid']!="undefined":
            item=UserListF.objects.get(id=int(data['listid']),user=request.user)
            if UserStat.get(data['status']):
                item.userstatus=UserStat[data['status']]
                item.save()

                sendFeed(item,typeFeed['status'])

                return JsonResponse({'status':'changestatus','userstatus':data['status']})
        else:
            return JsonResponse({'status':'false'})
    else:
        return JsonResponse({'status':'false'})