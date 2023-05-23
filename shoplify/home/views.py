from django.shortcuts import render
from products.models import *
from accounts.models import *

# Create your views here

def products(request):
    prod_obj = Product.objects.all()
    trending_pro = Product.objects.filter(is_trending = True)
    arrival_pro = Product.objects.filter(is_just_arrived = True)
    offer_pro = Product.objects.filter(is_offer = True)
        
    context = {
        'products': prod_obj,
        'trends': trending_pro,
        'arrives': arrival_pro,
        'offers': offer_pro,
        }
    

    return render(request, 'home/index.html', context)

def shop(request):
    products = Product.objects.all()

    size = SizeVariant.objects.all()

    context = {
        'products': products,
        }
    if request.method == "POST":
        check = request.POST.getlist('checkbox')

    return render(request, 'home/shop.html', context)
