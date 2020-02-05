from django.shortcuts import render,get_object_or_404
from Main.models import Serial,UserList,SeriesList
from django.db.models import Count

def serial(request,id):
    serial = get_object_or_404(Serial,id=id)

    seasons = serial.seasons
    fseason = seasons.first()
    if (fseason):
        try:
            fseason.date=SeriesList.objects.filter(season_id=fseason.id).order_by('date').first().date
        except AttributeError:
            dsicript = fseason.disctiption
            fseason = Fseason()
            fseason.disctiption = dsicript
    else:
        fseason = Fseason()


    if request.user.is_authenticated:
        for season in seasons:
            season.InMyList = UserList.objects.filter(user=request.user,season=season).exists()

    serial.seasonsl=seasons

    tags_ids = serial.tags.values_list('id', flat=True)
    similar_serials = Serial.objects.filter(tags__in=tags_ids) \
        .exclude(id=serial.id)

    similar_serials = similar_serials.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags')[:5]


    if request.method == 'POST':
        from Main.forms import CommentForm
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.item = serial
            new_comment.user= request.user
            new_comment.save()
            from django.shortcuts import redirect
            return redirect('serial',serial.id)
    else:
        from Main.forms import CommentForm
        comment_form = CommentForm()

    data={
        "serial":serial,
        "fseason":fseason,
        'similar_serials': similar_serials,
        "commentform": comment_form,
    }



    
    try:
        data.update({"UserItem":UserList.objects.filter(serial=id,user=request.user.id)})
    except UserList.DoesNotExist:
        pass
        
    return render(request,"Serials/serial.html",data)

class Fseason():
    disctiption="Нет данных"
    date="Нет данных"