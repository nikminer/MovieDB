from django.shortcuts import render, get_object_or_404
from MyWatchList.models import  WatchList
from MyWatchList.models import Movie
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def FilmList(request, page=1):
    FilmList = Movie.manager.get_films().order_by('-year')

    if request.is_ajax():
        return render(request, "Films/blocks/List_Ajax.html", {
            'urlname': 'filmlist_page',
            'items': ListFeature(request, page, FilmList)
        })
    else:
        return render(request, "Films/filmlist.html", {
            "List": ListFeature(request, page, FilmList),
        })


def FilmListSimilar(request, id, page=1):
    film = get_object_or_404(Movie, id=id)

    from django.db.models import Count
    tags_ids = film.tags.values_list('id', flat=True)
    similar_films = Movie.manager.get_films().filter(tags__in=tags_ids) \
        .exclude(id=film.id)
    FilmList = similar_films.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-rating')

    if request.is_ajax():
        return render(request, "Films/blocks/List_Ajax.html", {
            'urlname': 'filmsimilar_page',
            'items': ListFeature(request, page, FilmList),
        })
    else:
        return render(request, "Films/filmlistSimilar.html", {
            "film": film,
            "List": ListFeature(request, page, FilmList),
        })



def ListFeature(request,page,list):
    if request.GET.get('genres'):
        list = list.filter(tags__slug__in=request.GET.get('genres').split(' ')).distinct()

    paginator = Paginator(list, 20)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse(None)
        list = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        for item in list:
            item.InMyList = WatchList.objects.filter(movie=item, user=request.user).exists()

    return list