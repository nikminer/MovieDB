from django.contrib.sitemaps import Sitemap
from .models import Profile

class ProfileSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Profile.objects.all()
