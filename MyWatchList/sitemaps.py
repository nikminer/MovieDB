from django.contrib.sitemaps import Sitemap
from MyWatchList.models import Movie
from MyWatchList.models import Profile

class MoviesSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.4

    def items(self):
        return Movie.objects.all()

class ProfileSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Profile.objects.all()
