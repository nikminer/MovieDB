from django.contrib.sitemaps import Sitemap
from Main.models import Series

class SerialsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.4

    def items(self):
        return Series.objects.all()