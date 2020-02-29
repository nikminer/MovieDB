from django.urls import path
from django.conf.urls import include

from Films import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",views.filmlist.FilmList,name="filmlist"),
    path("<int:page>",views.filmlist.FilmList,name="filmlist_page"),
    path("details/<int:id>",views.film.film ,name="film"),
    path("details/<int:id>/similar",views.filmlist.FilmListSimilar,name="filmsimilar"),
    path("details/<int:id>/similar/<int:page>",views.filmlist.FilmListSimilar,name="filmsimilar_page"),
    path("set/status",views.film.setstatus),
    path("set/rating",views.film.setrating),
]