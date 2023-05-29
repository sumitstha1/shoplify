from django.contrib import admin
from .models import *
from django.contrib.admin import register


# Register your models here.
admin.site.register(UserProfile)


@register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_filter = ["is_paid", "user"]
    ordering = ["is_paid"]
    list_display = ["user", "is_paid"]

@register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ["cart", "product"]
    ordering = ["updated_at"]

@register(PaidCart)
class PaidCartAdmin(admin.ModelAdmin):
    list_filter = ["is_delivered", "user"]
    list_display = ["user", "is_delivered"]
    ordering = ["updated_at"]

@register(PaidCartItems)
class PaidCartItemsAdmin(admin.ModelAdmin):
    list_filter = ["cart"]
    list_display = ["cart", "product"]
    ordering = ["updated_at"]

@register(DeliveredCart)
class DeliveredCartAdmin(admin.ModelAdmin):
    list_display = ["user", "is_delivered"]
    ordering = ["updated_at"]

@register(DeliveredCartItems)
class DeliveredCartItemsAdmin(admin.ModelAdmin):
    # list_display = ["product__product_name"]
    # print("product__product_name")
    list_display = ["cart","product"]
    ordering = ["updated_at"]
    list_filter = ["updated_at"]


admin.site.register(WishList)
admin.site.register(WishlistItems)