from django.contrib import admin
from .models import Category, Home, Banner
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'catSlug': ('catName',)}
    list_display = ('catName', 'catSlug', 'catFor')
    search_fields = ['catName']
    list_filter = ('catName', 'catFor')


class HomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'keyword', 'description')


admin.site.register(Home, HomeAdmin)
admin.site.register(Banner)
admin.site.register(Category, CategoryAdmin)
