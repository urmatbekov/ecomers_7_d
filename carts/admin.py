from django.contrib import admin
from carts.models import Cart , CartItem
# Register your models here.
class CartItemInline(admin.TabularInline):
    model = CartItem
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [
        CartItemInline,
    ]
