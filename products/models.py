from accounts.models import Account
from app.models import Category
from django.db import models
from froala_editor.fields import FroalaField
from django.db.models import Avg

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

    def averageReview(self):
        reviews = ReviewRating.objects.filter(
            product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
            return avg


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


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField()
    rating = models.FloatField()
    ip = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
