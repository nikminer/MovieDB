from django.urls import path
from django.conf.urls import include

import Serials.src as src
from Serials.Seasons import urls as urlsSeasons

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', src.seriallist.SerialList,name='seriallist'),
    path('<int:id>',src.serial.serial,name='serial'),

    path('season/',include(urlsSeasons)),
]
