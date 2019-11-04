from django.contrib.sitemaps import Sitemap
from Main.models import Serial

class SerialsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.4

    def items(self):
        return Serial.objects.all()