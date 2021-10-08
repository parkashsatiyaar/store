from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from app.models import Home
from cart.models import Cart, CartItem
from django.http import HttpResponseRedirect
from products.models import Product, Variation

# Create your views here.


def _getCartId(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


@login_required(login_url='signin')
def addCartItem(request, productId):
    product = Product.objects.get(id=productId)
    if request.method == "POST":
        color = request.POST['color']
        size = request.POST['size']
    else:
        color = Variation.objects.filter(
            variationCategory="color", product=product).first().variationValue
        size = Variation.objects.filter(
            variationCategory="size", product=product).first().variationValue
    try:
        cart = Cart.objects.filter(cartId=_getCartId(request)).first()

    except Cart.DoesNotExist:
        cart = Cart.objects.create(cartId=_getCartId(request))
        cart.save()

    try:
        if request.user.is_authenticated:
            cartItem = CartItem.objects.get(
                product=product, user=request.user, itemColor=color, itemSize=size)
        else:
            cartItem = CartItem.objects.get(
                product=product, cart=cart, itemColor=color, itemSize=size)
        if product.productStock > cartItem.quantity:
            cartItem.quantity += 1
            cartItem.save()
    except CartItem.DoesNotExist:
        if request.user.is_authenticated:
            cartItem = CartItem.objects.create(
                product=product, user=request.user, cart=cart, quantity=1, itemColor=color,
                itemSize=size)
        else:
            cartItem = CartItem.objects.create(
                product=product, cart=cart, quantity=1, itemColor=color,
                itemSize=size)
        cartItem.save()
    return redirect('cart')


@login_required(login_url='signin')
def deleteCart(request):
    try:
        cart = Cart.objects.filter(cartId=_getCartId(request))
        if request.user.is_authenticated:
            cartitems = CartItem.objects.filter(user=request.user)
        else:
            cartitems = CartItem.objects.filter(cart=cart)
        cartitems.delete()
    except:
        cartitems = []

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='signin')
def deleteCartItem(request, productId):
    color = request.GET['color']
    size = request.GET['size']
    try:
        cart = Cart.objects.filter(cartId=_getCartId(request))
        if request.user.is_authenticated:
            cartitems = CartItem.objects.filter(
                user=request.user, product=productId, itemColor=color, itemSize=size)
        else:
            cartitems = CartItem.objects.filter(
                cart=cart, product=productId, itemColor=color, itemSize=size)
        cartitems.delete()
    except:
        cartitems = []
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='signin')
def cart(request, total=0, tax=0, grandTotal=0):
    home = Home.objects.all()
    try:
        cart = Cart.objects.filter(cartId=_getCartId(request))
        if request.user.is_authenticated:
            cartitems = CartItem.objects.filter(user=request.user)
        else:
            cartitems = CartItem.objects.filter(cart=cart)
        for cartItem in cartitems:
            total += (cartItem.product.ProductPrice*cartItem.quantity)
        tax = (5*total)/100
        grandTotal = total+tax
    except:
        cartitems = []
    context = {
        "total": total,
        "cartItems": cartitems,
        'tax': tax,
        'grandTotal': grandTotal,
        'homes': home,
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='signin')
def updateCart(request, productId):
    color = request.GET['color']
    size = request.GET['size']
    try:
        quantity = int(request.GET.get('quantity'))
        if quantity > 0:
            cart = Cart.objects.filter(cartId=_getCartId(request))
            if request.user.is_authenticated:
                cartitems = CartItem.objects.filter(
                    user=request.user, product=productId, itemColor=color, itemSize=size).first()
            else:
                cartitems = CartItem.objects.filter(
                    cart=cart, product=productId, itemColor=color, itemSize=size).first()
            if quantity <= cartitems.product.productStock:
                cartitems.quantity = quantity
                cartitems.save()
    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='signin')
def checkout(request, total=0, tax=0, grandTotal=0):
    home = Home.objects.all()
    try:
        cart = Cart.objects.filter(cartId=_getCartId(request))
        if request.user.is_authenticated:
            cartitems = CartItem.objects.filter(user=request.user)
        else:
            cartitems = CartItem.objects.filter(cart=cart)
        for cartItem in cartitems:
            total += (cartItem.product.ProductPrice*cartItem.quantity)
        tax = (5*total)/100
        grandTotal = total+tax
    except:
        cartitems = []
    context = {
        "total": total,
        "cartItems": cartitems,
        'tax': tax,
        'grandTotal': grandTotal,
        'homes': home,
    }
    return render(request, "store/checkout.html", context)
