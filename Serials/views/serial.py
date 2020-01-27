from django.shortcuts import render,get_object_or_404
from Main.models import Serial,Season,UserList,SeriesList
from django.db.models import Count

def serial(request,id):
    serial=get_object_or_404(Serial,id=id)
        
    fseason=serial.seasons.first()
    if (fseason):
        try:
            fseason.date=SeriesList.objects.filter(season_id=fseason.id).order_by('date').first().date
        except AttributeError:
            dsicript=fseason.disctiption
            fseason=Fseason()
            fseason.disctiption=dsicript
    else:
        fseason=Fseason()

    from django.db.models import Count
    tags_ids = serial.tags.values_list('id', flat=True)
    similar_serials = Serial.objects.filter(tags__in=tags_ids) \
        .exclude(id=serial.id)
    similar_serials = similar_serials.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags')[:5]

    data={
        "serial":serial,
        "fseason":fseason,
        'similar_serials': similar_serials
    }



    
    try:
        data.update({"UserItem":UserList.objects.filter(serial=id,user=request.user.id)})
    except UserList.DoesNotExist:
        pass
        
    return render(request,"Serials/serial.html",data)

class Fseason():
    disctiption="Нет данных"
    date="Нет данных"