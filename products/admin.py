from django.contrib import admin
from .models import Product, ProductGallery, Variation
import admin_thumbnails
# Register your models here.

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('productName', 'ProductPrice',
                    'productStock', 'productCategory', 'is_available')
    prepopulated_fields = {'productSlug': ('productName',)}
    list_filter = ('productCategory', 'is_available')
    search_fields = ['productName', 'productSiteDescription']
    list_editable = ('is_available',)

    inlines = [ProductGalleryInline]


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variationCategory', 'variationValue', 'is_active',
                    )
    list_filter = ('product', 'variationCategory',
                   'variationValue', 'is_active')
    search_fields = ['product__productName', 'product__productSiteDescription']
    list_editable = ('is_active',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
# admin.site.register(ProductGallery)
