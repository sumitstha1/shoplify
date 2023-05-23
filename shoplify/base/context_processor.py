from products.models import *
from accounts.models import *

def base_processor(request):
    categories = Category.objects.all()
    brands = Brands.objects.all()
    dresses = Dresses.objects.all()
    collection = Collection.objects.all()

    try:
        wishlist = WishList.objects.get(user = request.user)
        return {
            'categories': categories,
            'brands': brands,
            'dresses': dresses,
            'collections': collection,
            'wishlists': wishlist,
        }
    except:
        return {
            'categories': categories,
            'brands': brands,
            'dresses': dresses,
            'collections': collection,
        }


        