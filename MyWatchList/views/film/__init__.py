from . import filmlist

from django.shortcuts import render, get_object_or_404
from MyWatchList.models import Movie,WatchList

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

    if request.method == 'POST':
        from MyWatchList.forms import CommentForm
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.item = film
            new_comment.user = request.user
            new_comment.save()
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect(film.get_absolute_url())

    return render(request, "Films/film.html", data)

