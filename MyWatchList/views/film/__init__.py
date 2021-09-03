from . import filmlist

from django.shortcuts import render, get_object_or_404
from MyWatchList.models import Movie
from MyWatchList.models import WatchList

def film(request, id):
    film = get_object_or_404(Movie, id=id)
    if film.series:
        from django.shortcuts import redirect
        return redirect(film)

    data = {
        "film": film,
    }

    if not request.user.is_anonymous:
        try:
            data.update({"UserItem": WatchList.objects.get(movie=film, user=request.user)})
        except WatchList.DoesNotExist:
            pass

    

    return render(request, "Films/film.html", data)

