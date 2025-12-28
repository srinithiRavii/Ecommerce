from django.shortcuts import render,redirect,get_object_or_404
from store.models import Products
from . models import Cart,Cart_item
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart


def add_cart(request,product_id):
    product=Products.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cart_id(request))

    cart.save()
    try:
        cart_item=Cart_item.objects.get(product=product,cart=cart)
        cart_item.quantity+=1
        cart_item.save()
    except Cart_item.DoesNotExist:
        cart_item=Cart_item.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()
    return redirect('cart')
def remove_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Products,id=product_id)
    cart_item=Cart_item.objects.get(product=product,cart=cart)
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')
def remove_cart_item(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Products,id=product_id)
    cart_item=Cart_item.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')






def cart(request):
    total = 0
    quantity = 0
    cart_items = []

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = Cart_item.objects.filter(cart=cart, is_available=True)

        for cart_item in cart_items:
            total += cart_item.subtotal      # cart total
            quantity += cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist:
        pass

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax':tax,
        'grand_total':grand_total,
    }

    return render(request, "store/cart.html", context)




