from django.urls import path

from MyWatchList import views




urlpatterns = [
    path("filmlist", views.film.filmlist.FilmList, name="filmlist"),
    path("filmlist/<int:page>", views.film.filmlist.FilmList, name="filmlist_page"),

    path("details/<int:id>", views.film.film, name="film"),

    path("details/<int:id>/similar", views.film.filmlist.FilmListSimilar, name="filmsimilar"),
    path("details/<int:id>/similar/<int:page>", views.film.filmlist.FilmListSimilar, name="filmsimilar_page"),

    path("set/status", views.film.watchlistitems.setstatus),
    path("set/rating", views.film.watchlistitems.setrating),

    path('rewatch/inc', views.film.watchlistitems.increwatched),
    path('rewatch/set', views.film.watchlistitems.setrewatched),
    path("rewatch/dec", views.film.watchlistitems.decrewatched),
]