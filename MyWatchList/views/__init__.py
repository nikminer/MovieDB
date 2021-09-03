from . import film,series,list
from . import addmovie, decoratiors, ErrorsHandler

from MyWatchList.models import Profile
from MyWatchList.models import Movie
from django.db.models import Q
from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from MyWatchList.models import Movie, Season, CommentModel
from MyWatchList.forms.Comments import CommentForm, ReplyForm

def index(request):
    return render(request, "Main/index.html")

def searchPage(request):

    return render(request, "Main/search.html")

def search(request, query):
    series = Movie.manager.get_series().filter(Q(name__icontains=query) | Q(originalname__icontains=query))
    films = Movie.manager.get_films().filter(Q(name__icontains=query) | Q(originalname__icontains=query))
    users = Profile.objects.filter(Q(user__username__icontains=query) | Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query))

    return render(request, "Main/blocks/search_searchlist.html", {
        'series': series,
        'films': films,
        'users': users
    })

def AddCommentMovie(request, id):
    item = get_object_or_404(Movie, id=id)
    AddComment(request, item)

    return HttpResponseRedirect(item.get_absolute_url())


def AddCommentSeason(request, id):
    item = get_object_or_404(Season, id=id)
    AddComment(request, item)
    return HttpResponseRedirect(item.get_absolute_url())

def AddComment(request, item):
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.item = item
            new_comment.user = request.user
            new_comment.save()

def AddReplyComment(request, id):
    item = get_object_or_404(CommentModel, id=id)
    AddReply(request, item)
    return HttpResponseRedirect(item.get_absolute_url())

def AddReply(request, item):
    if request.method == 'POST':
        comment_form = ReplyForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.item = item
            new_comment.user = request.user
            new_comment.save()