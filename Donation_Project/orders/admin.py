from django.contrib import admin
from . models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['donation_type']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'cma', 'phone', 'address1',
                    'address2', 'city', 'state', 'postal', 'country', 'urbanization',
                    'created', 'updated', 'paid']

    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
