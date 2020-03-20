from django.shortcuts import render,get_object_or_404

from django.db.models import Count
from MyWatchList.models import Movie



def SeriesList(request,page=1):

    Serials=Movie.manager.get_series().order_by("-year", "name")

    data={
        "SerialList":ListFeature(request, page,Serials),
    }

    return render(request,"Serials/seriallist.html",data)



def SimilarSerials(request,id,page=1):
    serial = get_object_or_404(Movie, id=id)

    tags_ids = serial.tags.values_list('id', flat=True)
    similar_serials = Movie.manager.get_series().filter(tags__in=tags_ids) \
        .exclude(id=serial.id)
    Serials = similar_serials.annotate(same_tags=Count('tags')) \
        .order_by('-same_tags')

    data={
        "series":serial,
        "SerialList":ListFeature(request, page,Serials),
    }

    return render(request,"Serials/seriallistSimilars.html",data)


from MyWatchList.models import WatchList
from django.core.paginator import Paginator, EmptyPage

def ListFeature(request,page,list):
    if request.GET.get('genres'):
        list = list.filter(tags__slug__in=request.GET.get('genres').split(' ')).distinct()
    paginator = Paginator(list, 24)

    try:
        list = paginator.page(page)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        for item in list:
            item.InMyList = WatchList.objects.filter(movie=item, user=request.user).exists()
    return list