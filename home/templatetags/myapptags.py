from django import template
from django.urls import reverse
from home.models import Setting
from product.models import Category
from order.models import ShopCart

from django import template

register = template.Library()


@register.simple_tag
def categorylist():
    return Category.objects.all()


@register.simple_tag
def shopcartcount(userid):
    count = ShopCart.objects.filter(user_id=userid).count()
    return count