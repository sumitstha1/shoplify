from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from base.email import send_email_activation_token
import uuid
from products.models import *


# Create your models here.

class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.FileField(upload_to='profile')


    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid = False, cart__user = self.user).count()

    def get_wish_count(self):
        return WishlistItems.objects.filter(wish__user = self.user).count()

    def uid_getter(self):
        wish_item = []
        items = WishlistItems.objects.filter(wish__user = self.user)
        for item in items:
            print(item.product.product_name)
        return item.product.uid

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username

    def get_total_price(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.quantity * cart_item.product.selling_price)

        if self.coupon:
            if self.coupon.minimum_amount < sum(price):
                return sum(price) - self.coupon.discount_price

        return sum(price)



class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, blank=True, null=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=1)

    def get_product_price(self):
        price = self.product.selling_price
        quantity = self.quantity
        price = price * quantity
        return price

class WishList(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')


class WishlistItems(BaseModel):
    wish = models.ForeignKey(WishList, on_delete=models.CASCADE, related_name='wish_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.product.product_name



@receiver(post_save, sender = User)
def sent_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            UserProfile.objects.create(user = instance, email_token = email_token)
            email = instance.email
            send_email_activation_token(email, email_token)
    except Exception as e:
        print(e)


