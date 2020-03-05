from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from Main.models import Film,UserListF
from django.contrib.auth.decorators import login_required
from List.views.feed import sendFeed,typeFeed


def film(request,id):
    film = get_object_or_404(Film,id=id)

    from django.db.models import Count
    tags_ids = film.tags.values_list('id', flat=True)
    similar_films = Film.objects.filter(tags__in=tags_ids)\
        .exclude(id=film.id)
    similar_films = similar_films.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags', '-rating')[:5]

    if request.method == 'POST':
        from Main.forms import CommentForm
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.item = film
            new_comment.user= request.user
            new_comment.save()
            from django.shortcuts import redirect
            return redirect('film',film.id)
    else:
        from Main.forms import CommentForm
        comment_form = CommentForm()

    data = {
        "Film": film,
        'similar_films': similar_films,
        "commentform": comment_form,
    }
    
    try:
        data.update({"UserItem": UserListF.objects.get(film_id=id, user=request.user.id)})
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

@login_required
def increwatched(request):
    item = UserListF.objects.get(id=int(request.POST['listid']), user=request.user.id)
    item.countreview += 1
    item.save()
    return JsonResponse({'status': 'inc', "countreview": item.countreview})

@login_required
def decrewatched(request):
    item = UserListF.objects.get(id=int(request.POST['listid']), user=request.user.id)

    if item.countreview - 1 >= 0:
        item.countreview -= 1
        item.save()
        return JsonResponse({'status': 'inc', "countreview": item.countreview})

    else:
        return JsonResponse({'status': 'false', "countreview": item.countreview})

@login_required
def setrewatched(request):
    item = UserListF.objects.get(id=int(request.POST['listid']), user=request.user.id)
    ep = int(request.POST['count'])
    if not ep < 0:
        item.countreview = ep
        item.save()
        return JsonResponse({'status': 'inc', "countreview": item.countreview})
    else:
        return JsonResponse({'status': 'false', "countreview": item.countreview})