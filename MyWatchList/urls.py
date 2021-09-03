from django.urls import path
from django.conf.urls import include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from MyWatchList.views.series import urls as urlsSeries
from MyWatchList.views.film import urls as urlsFilms
from MyWatchList.views.list import urls as urlsList

from MyWatchList import views

urlpatterns = [

    path('serial/',include(urlsSeries),),
    path('film/',include(urlsFilms)),
    path('list/',include(urlsList), name='list'),


   ]
