from django.shortcuts import render, get_object_or_404
from Main.models import UserList,Season,SeriesList

def season(request,id):
    season=get_object_or_404(Season,id=id)
    try:
        season.date= SeriesList.objects.filter(season_id=id).order_by('date').first().date
    except AttributeError:
        season.date="Нет данных"

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

    data={
        "season":season,
        "commentform": comment_form,
    }
    try:
        data.update({"UserItem":UserList.objects.get(season=season,user=request.user.id)})
    except UserList.DoesNotExist:
        pass

    return render(request,"Serials/season.html",data)