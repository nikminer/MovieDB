from . import numeric,change

from django.shortcuts import render, get_object_or_404
from MyWatchList.models import WatchList,Season,SeriesList

def season(request,id):
    season=get_object_or_404(Season,id=id)

    '''
    if request.method == 'POST':
        from Main.forms import CommentForm
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.item = season
            new_comment.user= request.user
            new_comment.save()
            from django.shortcuts import redirect
            return redirect('season',season.id)
    else:
        from Main.forms import CommentForm
        comment_form = CommentForm()
    "commentform": comment_form,
    '''

    data={
        "season":season,
    }

    try:
        data.update({"UserItem":WatchList.objects.get(season=season,user=request.user.id)})
    except WatchList.DoesNotExist:
        pass

    return render(request,"Serials/season.html",data)