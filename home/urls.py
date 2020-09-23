from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from home import views
from .sitemaps import ProductSitemap, StaticViewSitemap, CategorySitemap

sitemaps = {
    'product' : ProductSitemap,
    'static': StaticViewSitemap,
    'category': CategorySitemap,

}

urlpatterns = [
    path('', views.index, name="index"),
    path('home/', views.index, name="index"),
    path('order_confirmation/', views.order_confirmation, name="order_confirmation"),
    path('about/', views.aboutus, name='aboutus'),
    path('contact/', views.contactus, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('pay/', views.pay, name='pay'),
    path('prodinfo/', views.prodinfo, name='prodinfo'),
    path('category/', views.category, name='category'),
    path('prodinfo/', views.prodinfo, name='prodinfo'),
    # path('gallery/', views.gallery, name='gallery'),
    # path('pricing/', views.pricing, name='pricing'),


    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
  


]