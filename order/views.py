from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.crypto import get_random_string

from home.models import Setting
from order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from product.models import Category, Product, Variants
from user.models import UserProfile


def index(request):
    return HttpResponse("order Page")


def addtoshopcart(request,id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    variantid = request.POST.get('variantid')
    checkinproduct = ShopCart.objects.filter(product_id=id)
    checkinvariant = ShopCart.objects.filter(variant_id=variantid)

    if checkinproduct and checkinvariant:
        control = 1  # the product is in cart
    else:
        control = 0  # the product is not in cart

    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, " Product Added to Shopping Cart ")
        return HttpResponseRedirect(url)

    else:  # if there is no post
        if control == 1:  # Update shopcart
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()  #
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.variant_id = None
            data.save()
        messages.success(request, " Product Added To ShopCart")
        return HttpResponseRedirect(url)


def shopcart(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity

    context = {
        'shopcart': shopcart,
        'setting': setting,
        'total': total,
        'category': category
    }

    return render(request, 'shopcart_products.html', context)


def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "your item deleted! for Cart")
    return HttpResponseRedirect("/shopcart")


def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():

            # apply credit card infromation from the bank like api process
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.code = ordercode 
            data.save()

            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                if rs.product.variant == 'None':
                    detail.price = rs.product.price
                else:
                    detail.price = rs.variant.price
                detail.variant_id = rs.variant_id
                detail.amount = rs.amount
                detail.save()

                if rs.product.variant == 'None':
                    product = Product.objects.get(id=rs.product_id)
                    product.amount -= rs.quantity
                    product.save()
            else:
                check = Variants.objects.filter(id=rs.product_id)
                if len(check) > 0:
                    variant = Variants.objects.get(id=rs.product_id)
                    variant.quantity -= rs.quantity
                    variant.save()

            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(request, "Your Order has been completed. Thank static")
            return render(request, 'order_completed.html', {'ordercode': ordercode, 'category': category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    setting = Setting.objects.get(pk=1)
    context = {
        'shopcart': shopcart,
        'setting': setting,
        'total': total,
        'form': form,
        'profile': profile,
        'category': category,
    }
    return render(request, 'order_form.html', context)

