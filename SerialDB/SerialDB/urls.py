from django.urls import path
from django.conf.urls import include, url

from django.conf import settings
from django.conf.urls.static import static

from Main import views

from Serials import urls as urlsSerials
from List import urls as urlsList
from Films import urls as urlsFilms
from Profile import urls as urlsProfile
from Profile.views.auth import loginView

urlpatterns = [
    path('',views.index.index,name="index"),
    path('add/',views.addmovie.AddMoviePage,name='addmovie'),
    path('add/kinopoisk/search/',views.addmovie.Search),
    path('add/kinopoisk/<int:id>/',views.addmovie.AddMovie),

    path('list/',include(urlsList), name='list'),
    path('serial/',include(urlsSerials), name='serial'),
    path('film/',include(urlsFilms), name='film'),
    path('profile/',include(urlsProfile), name='profile'),
    path('accounts/login/', loginView, name='login'),
   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
