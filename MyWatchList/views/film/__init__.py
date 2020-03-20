from . import filmlist,watchlistitems

from django.shortcuts import render, get_object_or_404
from MyWatchList.models import Movie,WatchList

def film(request, id):
    film = get_object_or_404(Movie, id=id)
    if film.series:
        from django.shortcuts import redirect
        return redirect(film)

    '''
    if request.method == 'POST':
        from Main.forms import CommentForm
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.item = film
            new_comment.user = request.user
            new_comment.save()
            from django.shortcuts import redirect
            return redirect('film', film.id)
    else:
        from Main.forms import CommentForm
        comment_form = CommentForm()

    data = {
        "film": film,
        "commentform": comment_form,
    }
    '''
    data = {
        "film": film,
    }

    try:
        data.update({"UserItem": WatchList.objects.get(movie=film, user=request.user)})
    except WatchList.DoesNotExist:
        pass

    return render(request, "Films/film.html", data)

