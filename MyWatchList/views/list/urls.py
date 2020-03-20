from django.urls import path
from List import views
from MyWatchList.views import list

urlpatterns = [
    path('<str:username>/series', list.watchlist_series ,name='listserial'),

    path('add/serial/<int:id>', views.serials.AddSerial,name='addserial'),
    path('del/serial/<int:id>',views.serials.DelSerial,name='delserial'),


    path('<str:username>/films', list.watchlist_films,name='listfilm'),

    path('add/film/<int:id>', views.film.AddFilm,name='addfilm'),
    path('del/film/<int:id>', views.film.DelFilm,name='delfilm'),
]
