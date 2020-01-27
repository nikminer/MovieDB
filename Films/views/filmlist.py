from django.shortcuts import render
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