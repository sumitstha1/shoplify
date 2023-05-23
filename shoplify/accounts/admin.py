from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(WishList)
admin.site.register(WishlistItems)