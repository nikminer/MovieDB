from django.shortcuts import render,get_object_or_404
from Main.models import Film,UserListF
from django.core.paginator import Paginator, EmptyPage

def FilmList(request,page=1):
    FilmList=Film.objects.all().order_by('-year') 

    if request.GET.get('genres'):
       FilmList= FilmList.filter(tags__slug__in=request.GET.get('genres').split(' ')).distinct()

    paginator = Paginator(FilmList, 24)

    try:
        FilmList = paginator.page(page)
    except EmptyPage:
        FilmList = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        for film in FilmList:
            film.InMyList=str(len(UserListF.objects.filter(film=film,user=request.user))>0)
    
    data={
        "FilmList":FilmList,
    }
    return render(request,"Films/filmlist.html",data)


def FilmListSimilar(request,id, page=1):

    film = get_object_or_404(Film, id=id)

    from django.db.models import Count
    tags_ids = film.tags.values_list('id', flat=True)
    similar_films = Film.objects.filter(tags__in=tags_ids) \
        .exclude(id=film.id)
    FilmList = similar_films.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-rating')


    if request.GET.get('genres'):
        FilmList = FilmList.filter(tags__slug__in=request.GET.get('genres').split(' ')).distinct()

    paginator = Paginator(FilmList, 24)

    try:
        FilmList = paginator.page(page)
    except EmptyPage:
        FilmList = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        for i in FilmList:
            i.InMyList = str(len(UserListF.objects.filter(film=film, user=request.user)) > 0)

    data = {
        "film":film,
        "FilmList": FilmList,
    }
    return render(request, "Films/filmlistSimilar.html", data)