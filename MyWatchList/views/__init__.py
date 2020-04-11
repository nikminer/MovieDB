from . import film,series,list

from . import addmovie, decoratiors, ErrorsHandler


from django.shortcuts import render

def index(request):

    return render(request, "Main/index.html")
