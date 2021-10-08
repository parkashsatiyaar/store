from django.urls.conf import path
from . import views
urlpatterns = [
    path('', views.cart, name='cart'),
    path('add-cart/<int:productId>', views.addCartItem, name="addCart"),
    path('clear-cart/', views.deleteCart, name="deleteCart"),
    path('clear-cart-item/<int:productId>',
         views.deleteCartItem, name="deleteCartItem"),
    path('update-cart/<int:productId>/',
         views.updateCart, name="updateCart"),
    path('checkout/',views.checkout, name="checkout" )
]
