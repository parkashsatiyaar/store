from django.contrib import admin

from orders.models import Order, OrderProduct, Payment

# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['payment', 'user',
                       'product', 'quantity', 'product_price', 'size', 'color']
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'first_name', 'last_name',
                    'is_ordered', 'status')

    list_filter = ('status', 'is_ordered', 'created_date', 'updated_date')
    list_editable = ('status',)
    search_fields = ['order_number', 'first_name',
                     'last_name', 'phone', 'email', 'address_line_1', 'state', 'city', 'country']

    list_per_page = 20

    inlines = [OrderProductInline]


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
