from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'completed', 'transaction_id')
    search_fields = ('customer', 'transaction_id') 

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('customer', 'bought', 'product', 'transaction_id', 'delivered')
    search_fields = ('customer', 'transaction_id') 

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'delivery_date')
    search_fields = ('customer', 'address')

admin.site.register(Account, AccountAdmin)
admin.site.register(Customer)
admin.site.register(CategoryType)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart, CartAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(SavedProduct)
admin.site.register(Comment)
admin.site.register(Payment)
admin.site.register(Enquiry)