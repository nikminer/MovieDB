from django.urls import path
from django.conf.urls import include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from Profile import urls as urlsProfile

from MyWatchList.views.series import urls as urlsSeries
from MyWatchList.views.film import urls as urlsFilms
from MyWatchList.views.list import urls as urlsList
from MyWatchList import views as MWView

from django.contrib.sitemaps.views import sitemap

from Profile.sitemaps import ProfileSitemap
from MyWatchList.sitemaps import MoviesSitemap


handler404 = MWView.ErrorsHandler.error_404


sitemaps = {
    'profiles': ProfileSitemap,
    'movies': MoviesSitemap
}



urlpatterns = [
    path('', MWView.index, name="index"),

    path('add/', MWView.addmovie.AddMoviePage, name='addmovie'),
    path('add/kinopoisk/search/', MWView.addmovie.Search),
    path('add/kinopoisk/<int:id>/', MWView.addmovie.AddMovie),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),


    path('serial/',include(urlsSeries),),
    path('film/',include(urlsFilms)),

    path('list/',include(urlsList), name='list'),

    path('profile/',include(urlsProfile), name='profile'),
    path('admin/', admin.site.urls),


   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
