from django.urls import path
from MyWatchList.views import list

urlpatterns = [
    path('<str:username>/series', list.watchlist_series, name='listserial'),
    path('<str:username>/films', list.watchlist_films,name='listfilm'),

    path('add/<int:movie_id>', list.addlist, name='addlist'),
    path('del/<int:movie_id>', list.dellist, name='dellist'),
]
