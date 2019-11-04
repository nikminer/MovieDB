from django.urls import path
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from Main import views

from Serials import urls as urlsSerials
from List import urls as urlsList
from Films import urls as urlsFilms
from Profile import urls as urlsProfile
from Profile.views.auth import loginView

from django.contrib.sitemaps.views import sitemap
from Profile.sitemaps import ProfileSitemap
from Films.sitemaps import FilmsSitemap
from Serials.sitemaps import SerialsSitemap

sitemaps = {
    'profiles': ProfileSitemap,
    'films':FilmsSitemap,
    'seials':SerialsSitemap
}


urlpatterns = [
    path('',views.index.index,name="index"),
    path('add/',views.addmovie.AddMoviePage,name='addmovie'),
    path('add/kinopoisk/search/',views.addmovie.Search),
    path('add/kinopoisk/<int:id>/',views.addmovie.AddMovie),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),

    path('list/',include(urlsList), name='list'),
    path('serial/',include(urlsSerials), name='serial'),
    path('film/',include(urlsFilms), name='film'),
    path('profile/',include(urlsProfile), name='profile'),
    path('accounts/login/', loginView, name='login'),
   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
