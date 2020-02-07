from django.urls import path
from django.conf.urls import include

import Serials.views as views
from Serials.Seasons import urls as urlsSeasons


urlpatterns = [
    path('', views.seriallist.SerialList, name='seriallist'),
    path('<int:page>', views.seriallist.SerialList, name='seriallist_page'),

    path('details/<int:id>', views.serial.serial, name='serial'),

    path('details/<int:id>/similar', views.seriallist.SimilarSerials, name='Similarserial'),
    path('details/<int:id>/similar/<int:page>', views.seriallist.SimilarSerials, name='Similarserial_page'),

    path('season/',include(urlsSeasons)),
]
