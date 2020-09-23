from django.contrib.sitemaps import Sitemap
from product.models import Category, Product
from django.shortcuts import reverse



class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Category.objects.all()


class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Product.objects.all()


class StaticViewSitemap(Sitemap):
    protocol = "https"
    
    def items(self):
        return [
            'index',
            'aboutus',
            'category',
            'faq',
            'pay',
        ]

    def location(self, item):
        return reverse(item)


