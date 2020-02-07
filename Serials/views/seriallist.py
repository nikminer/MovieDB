from django.shortcuts import render,get_object_or_404
from Main.models import Serial,UserList
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count

def SerialList(request,page=1):

    Serials=Serial.objects.all().order_by("-year", "name")

    if request.GET.get('genres'):
       Serials= Serials.filter(tags__slug__in =request.GET.get('genres').split(' ')).distinct()

    paginator = Paginator(Serials, 24)

    try:
        Serials = paginator.page(page)
    except EmptyPage:
        Serials = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        for serial in Serials:
            serial.InMyList=UserList.objects.filter(serial=serial,user=request.user).exists()

    data={
        "SerialList":Serials,
    }


    return render(request,"Serials/seriallist.html",data)



def SimilarSerials(request,id,page=1):
    serial = get_object_or_404(Serial, id=id)

    tags_ids = serial.tags.values_list('id', flat=True)
    similar_serials = Serial.objects.filter(tags__in=tags_ids) \
        .exclude(id=serial.id)
    Serials = similar_serials.annotate(same_tags=Count('tags')) \
                          .order_by('-same_tags')

    if request.GET.get('genres'):
       Serials= Serials.filter(tags__slug__in =request.GET.get('genres').split(' ')).distinct()

    paginator = Paginator(Serials, 24)

    try:
        Serials = paginator.page(page)
    except EmptyPage:
        Serials = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        for i in Serials:
            i.InMyList=UserList.objects.filter(serial=serial,user=request.user).exists()

    data={
        "serial":serial,
        "SerialList":Serials,
    }


    return render(request,"Serials/seriallistSimilars.html",data)
