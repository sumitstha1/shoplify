from django.contrib import admin
from .models import *

# Register your models here.
class ProductImageAdmin(admin.StackedInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'actual_price', 'is_trending', 'is_offer', 'is_just_arrived', 'in_stock']
    inlines = [ProductImageAdmin]

admin.site.register(ColorVariant)

admin.site.register(SizeVariant)

admin.site.register(Brands)

admin.site.register(Category)

admin.site.register(Dresses)

admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImages)

admin.site.register(Collection)

admin.site.register(ProductReview)

admin.site.register(ProductMessage)

admin.site.register(Coupon)