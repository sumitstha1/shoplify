from django.shortcuts import render
from .models import *

# Create your views here.
def get_product(request, slug):
    product = Product.objects.get(slug = slug)
    try:
        product_review = ProductReview.objects.get(product = product)
        context = {'products': product, 'reviews': product_review}

        return render(request, 'products/product.html', context)

    except:
        context = {'products': product}
        return render(request, 'products/product.html', context)

    finally:
        if request.GET.get('size'):
            size = request.GET.get('size')
            

            context['selected_size'] = size

        if request.GET.get('color'):
            color = request.GET.get('color')

            context['selected_color'] = color
        return render(request, 'products/product.html', context)


def dress_product(request, slug):
    try:
        dress_product = Dresses.objects.get(slug = slug)

        context = {
            'dress': dress_product
        }
        return render(request, 'products/dress_product.html', context)

    except Exception as e:
        print(e)

def category_product(request, slug):
    try:
        category_product = Category.objects.get(slug = slug)

        context = {
            'category': category_product
        }
        return render(request, 'products/category_product.html', context)

    except Exception as e:
        print(e)