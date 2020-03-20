from . import seriallist
from django.shortcuts import render, get_object_or_404
from MyWatchList.models import Movie,WatchList

def series(request, id):
    series = get_object_or_404(Movie, id=id)

    if not series.series:
        from django.shortcuts import redirect
        return redirect(series)

    seasons = series.get_seasons()

    if request.user.is_authenticated:
        for season in seasons:
            season.InMyList = WatchList.objects.filter(user=request.user, season=season).exists()


    '''
       
    if request.method == 'POST':
        from Main.forms import CommentForm
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.item = serial
            new_comment.user = request.user
            new_comment.save()
            from django.shortcuts import redirect
            return redirect('serial', serial.id)
    else:
        from Main.forms import CommentForm
        comment_form = CommentForm()
        
        "commentform": comment_form,
    '''

    data = {
        "series": series,
        "seasons":seasons,
    }

    try:
        data.update({"UserItem": WatchList.objects.filter(movie=series, user=request.user)})
    except WatchList.DoesNotExist:
        pass

    return render(request, "Serials/series.html", data)