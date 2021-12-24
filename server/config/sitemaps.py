from django.contrib.sitemaps import Sitemap
from apps.main.models import Ad


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Ad.objects.filter(archive=False)

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return f'/ads/{obj.id}'
