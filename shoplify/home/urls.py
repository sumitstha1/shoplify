from django.urls import path
from .views import *
from products.views import *

urlpatterns = [
    path('', products, name='product'),
    path('shop/', shop, name='shop'),
    path('dress/<slug>/', dress_product, name='dress_product'),
    path('category/<slug>/', category_product, name='category_product'),
]
