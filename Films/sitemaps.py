from django.contrib.sitemaps import Sitemap
from Main.models import Film

class FilmsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.4

    def items(self):
        return Film.objects.all()
