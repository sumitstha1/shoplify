from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import *

# Create your views here.
def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Sorry! Your account is not registered yet.')
            return HttpResponseRedirect(request.path_info)

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Sorry! Your account is not verified yet.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username = email, password = password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/login.html')

def register_page(request):
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        profile_image = request.POST.get('profile_image')

        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already exists')
            return HttpResponseRedirect(request.path_info)

        
        user_obj = User.objects.create(first_name = first_name, last_name = last_name, email = email, password = password, username = email)
        user_obj.set_password(password)
        user_obj.save()
        user = UserProfile.objects.get(user = user_obj.id)
        user.profile_image = profile_image
        user.save()
        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)
    
    return render(request, 'accounts/register.html')

def activate_email(request, email_token):
    try:
        user = UserProfile.objects.get(email_token = email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        print(e)


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    return render(request, 'accounts/logout.html')


def user_review(request, uid):
    if request.method == "POST":
        if request.user.is_authenticated:
            product = Product.objects.get(uid = uid)
            product_review,_ = ProductReview.objects.get_or_create(product = product)
            message = request.POST.get('message')
            name = request.POST.get('name')
            email = request.POST.get('email')
            review_message = ProductMessage.objects.create(review = product_review, name = name, email = email, message = message)

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            return redirect('login')
        


def add_to_cart(request, uid):
    if request.method == "POST":
        if request.POST.get('size') and request.POST.get('color'):
            
            product = Product.objects.get(uid = uid)
            user = request.user
            cart, _ = Cart.objects.get_or_create(user = user, is_paid = False)
            cart_item = CartItems.objects.create(cart = cart, product = product)
            size = request.POST.get('size')
            size_variant = SizeVariant.objects.get(size = size)
            cart_item.size_variant = size_variant
            color = request.POST.get('color')
            color_variant = ColorVariant.objects.get(color = color)
            cart_item.color_variant = color_variant
            quantity = request.POST.get('quantity')
            cart_item.quantity = quantity
            cart_item.save()

        
        

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        messages.warning(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)


def remove_cart(request, uid):
    try:
        cart_item = CartItems.objects.get(uid = uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart(request):
    try:
        cart = Cart.objects.get(is_paid = False, user = request.user)
        if request.method == 'POST':
            coupon = request.POST.get('coupon')
            coupon_obj = Coupon.objects.filter(coupon_code = coupon)

            if not coupon_obj.exists():
                messages.warning(request, 'Invalid Coupon Code!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if cart.coupon:
                messages.warning(request, 'Coupon already exists!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            if cart.get_total_price() < coupon_obj[0].minimum_amount:
                messages.warning(request, f'Amount must be greater than {coupon_obj[0].minimum_amount}!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if coupon_obj[0].is_expired:
                messages.warning(request, f'Coupon is expired!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


            cart.coupon = coupon_obj[0]
            cart.save()

            messages.success(request, 'Coupon applied!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        return render(request, 'accounts/cart.html')
          
    context = {
        'carts': cart
    }
    return render(request, 'accounts/cart.html', context)

def remove_coupon(request, cart_id):
    cart = Cart.objects.get(uid = cart_id)
    cart.coupon = None
    cart.save()
    messages.success(request, 'Coupon removed successfully!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_to_wishlist(request, uid):
    try:
        product = Product.objects.get(uid = uid)
        user = request.user
        wishlist, _ = WishList.objects.get_or_create(user = user)
        wish_item = WishlistItems.objects.filter(wish = wishlist, product = product)
        if wish_item.exists():
            wish_item.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        wish_item = WishlistItems.objects.create(wish = wishlist, product = product)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except:
        messages.warning(request, 'You must login to add item to wishlist.')
        return redirect('login')

def wishlist(request):
    try:
        wish_item = WishList.objects.get(user = request.user)

    except Exception as e:
        return render(request, 'accounts/wishlist.html')
    
    context = {
        'wish': wish_item
    }
    return render(request, 'accounts/wishlist.html', context)