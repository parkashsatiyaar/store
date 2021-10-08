from django.db import models
from products.models import Product, Variation
from accounts.models import Account
# Create your models here.


class Cart(models.Model):
    cartId = models.CharField(max_length=250, blank=True)
    data_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cartId


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    itemColor = models.CharField(max_length=50, blank=True)
    itemSize = models.CharField(max_length=50, blank=True)
    cart = models.ForeignKey(Cart,
                             on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def subTotal(self):
        return self.product.ProductPrice*self.quantity

    def __str__(self):
        return f"{self.product}"
