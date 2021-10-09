from django.db import models
from froala_editor.fields import FroalaField
# Create your models here.


class Home(models.Model):
    title = models.CharField(max_length=200, unique=True)
    keyword = models.TextField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Home"
        verbose_name_plural = "Home"

    def __str__(self):
        return self.title


class Banner(models.Model):
    title = models.CharField(max_length=200, unique=True)
    subTitle = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="Images/banners/")

    def __str__(self):
        return self.title


choice_for_catFor = (
    ('M', 'M'),
    ('F', 'F'),
    ('C', 'C'),
)


class Category(models.Model):
    catName = models.CharField(max_length=100, unique=True)
    catSlug = models.SlugField(max_length=100, unique=True)
    catFor = models.CharField(
        max_length=50, choices=choice_for_catFor, default='M')
    description = FroalaField(blank=True)
    image = models.ImageField(
        upload_to="Images/category/", null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.catName
