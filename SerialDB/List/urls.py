from django.urls import path
from List import views

urlpatterns = [
    path('<str:username>/serials', views.serials.userlist,name='listserial'),

    path('add/serial/<int:id>', views.serials.AddSerial,name='addserial'),
    path('del/serial/<int:id>',views.serials.DelSerial,name='delserial'),


    path('<str:username>/films', views.film.userlist,name='listfilm'),

    path('add/film/<int:id>', views.film.AddFilm,name='addfilm'),
    path('del/film/<int:id>', views.film.DelFilm,name='delfilm'),
]
