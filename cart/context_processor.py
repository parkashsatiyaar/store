from .models import Cart, CartItem
from.views import _getCartId


def counter(request):
    if 'secureAdmin' in request.path:
        return {}
    else:
        try:
            total = 0
            cartCount = 0
            grandTotal = 0
            tax = 0
            cart = Cart.objects.filter(cartId=_getCartId(request))
            if request.user.is_authenticated:
                cartItems = CartItem.objects.filter(user=request.user)
            else:
                cartItems = CartItem.objects.filter(cart=cart)
            cartCount = cartItems.count()
            for cartItem in cartItems:
                total += (cartItem.product.ProductPrice * cartItem.quantity)
            tax = (5*total)/100
            grandTotal = total+tax
        except:
            cart = {}
            cartItems = {}
    return {'cartCount': cartCount, 'cartItems': cartItems, 'grandTotal': grandTotal}
