from django.contrib.sitemaps import Sitemap
from MyWatchList.models import Movie

class MoviesSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.4

    def items(self):
        return Movie.objects.all()
