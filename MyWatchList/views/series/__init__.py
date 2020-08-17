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