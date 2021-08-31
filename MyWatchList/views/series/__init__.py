from . import seriallist
from django.shortcuts import render, get_object_or_404
from MyWatchList.models import Movie
from MyWatchList.models import WatchList

def series(request, id):
    series = get_object_or_404(Movie, id=id)

    if not series.series:
        from django.shortcuts import redirect
        return redirect(series)

    seasons = series.get_seasons()

    if request.user.is_authenticated:
        for season in seasons:
            season.InMyList = WatchList.objects.filter(user=request.user, season=season).exists()


    if request.method == 'POST':
        from MyWatchList.forms import CommentForm
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.item = series
            new_comment.user = request.user
            new_comment.save()
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect(series.get_absolute_url())


    data = {
        "series": series,
        "seasons": seasons,
    }
    if not request.user.is_anonymous:
        try:
            data.update({"UserItem": WatchList.objects.filter(movie=series, user=request.user)})
        except WatchList.DoesNotExist:
            pass

    return render(request, "Serials/series.html", data)