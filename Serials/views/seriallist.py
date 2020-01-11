from django.shortcuts import render
from Main.models import Serial,UserList
from django.core.paginator import Paginator, EmptyPage

def SerialList(request,page=1):

    Serials=Serial.objects.all().order_by("-year", "name")

    if request.GET.get('genres'):
       Serials= Serials.filter(genre__genre__tag__in=request.GET.get('genres').split(' ')).distinct()

    paginator = Paginator(Serials, 24)

    try:
        Serials = paginator.page(page)
    except EmptyPage:
        Serials = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        for serial in Serials:
            serial.InMyList=str(len(UserList.objects.filter(serial=serial,user=request.user))>0)

    data={
        "SerialList":Serials,
    }


    return render(request,"Serials/seriallist.html",data)
