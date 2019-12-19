from django.urls import path
from django.conf.urls import include

from Films import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",views.filmlist.FilmList,name="filmlist"),
    path("<int:id>",views.film.film ,name="film"),
    path("set/status",views.film.setstatus),
    path("set/rating",views.film.setrating),
]