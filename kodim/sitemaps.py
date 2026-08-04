from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from Web_1.models import Course, News


class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Course.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('course', args=[obj.name_url])


class NewsSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return News.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.published_date

    def location(self, obj):
        return reverse('news-detail', args=[obj.slug])


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return ['home', 'about', 'courses', 'news', 'contact-us']

    def location(self, item):
        return reverse(item)
