from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from home.models import Setting, FAQ
from product.models import Category, Product


def index(request):
    return HttpResponse("User App")


def faq(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    faq = FAQ.objects.filter(status="True").order_by("ordernumber")
    products_top2 = Product.objects.all().order_by('?')[:4]
    context = {'faq': faq,
               'setting': setting,
               'category': category,
               'products_top2': products_top2,
               }

    return render(request, 'faq.html', context)
