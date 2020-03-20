from django.urls import path
from django.conf.urls import include

from MyWatchList.views import series
from MyWatchList.views.series.seasons import urls as urlsSeasons


urlpatterns = [
    path('', series.seriallist.SeriesList, name='seriallist'),
    path('<int:page>', series.seriallist.SeriesList, name='seriallist_page'),

    path('details/<int:id>', series.series, name='serial'),

    path('details/<int:id>/similar', series.seriallist.SimilarSerials, name='Similarserial'),
    path('details/<int:id>/similar/<int:page>', series.seriallist.SimilarSerials, name='Similarserial_page'),

    path('season/',include(urlsSeasons)),
]
