from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('activate/<email_token>', activate_email, name='activate_email'),
    path('logout/', logout_page, name='logout'),
    path('add-review/<uid>/', user_review, name='reviews'),
    path('add-to-cart/<uid>/', add_to_cart, name='add_to_cart'),
    path('remove-cart/<uid>/', remove_cart, name='remove_cart'),
    path('add-to-wishlist/<uid>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', wishlist, name='wishlist'),
    path('cart/', cart, name='cart'),
    path('remove-coupon/<cart_id>/', remove_coupon, name="remove_coupon"),
]
