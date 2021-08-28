from . import film,series,list

from . import addmovie, decoratiors, ErrorsHandler

from Profile.models import Profile
from MyWatchList.models import Movie
from django.db.models import Q 
from django.shortcuts import render

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