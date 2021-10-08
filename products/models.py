from app.models import Category
from django.db import models
from froala_editor.fields import FroalaField


# Create your models here.


class Product(models.Model):
    productName = models.CharField(max_length=200, unique=True)
    productTitle = models.CharField(max_length=200, unique=True)
    productKeyword = models.TextField(blank=True)
    productSlug = models.SlugField(unique=True)
    productDescription = FroalaField()
    productSiteDescription = models.TextField(blank=True)
    ProductPrice = models.FloatField()
    productImage = models.ImageField(upload_to="Images/products/%Y/%m/%d/")
    productStock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    productCategory = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.productName


variationCategory = (
    ('color', 'color'),
    ('size', 'size'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variationCategory = models.CharField(
        max_length=50, choices=variationCategory)
    variationValue = models.CharField(
        max_length=50, default="black")
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.variationValue


class ProductGallery(models.Model):
    product = models.ForeignKey(
        Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products')

    def __str__(self):
        return self.product.productName

    class Meta:
        verbose_name = 'product gallery'
        verbose_name_plural = 'product gallery'
