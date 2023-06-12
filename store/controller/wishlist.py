from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import *


@login_required(login_url='loginpage')
def viewWishList(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist': wishlist}
    return render(request,'store/wishListView.html', context)

def addToWishList(request,product_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_check = Product.objects.get(id=product_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user,product_id=product_id)):
                    messages.warning(request,'Product already in wishlist')                    
                else:
                    Wishlist.objects.create(user=request.user, product_id=product_id)
                    messages.success(request, 'Product wishlisted')                        
            else:
                messages.error(request, 'No such product found')
        else:
            messages.error(request, 'Login for wishlisting a product')
            return redirect('loginpage')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='loginpage')
def deleteWishlistItem(request,product_id):
    if request.method == 'POST':
        wishlist_item = Wishlist.objects.get(id=product_id)
        if wishlist_item:
            wishlist_item.delete()
            messages.success(request, 'item deleted')
            return redirect('viewWishList')
        else:
            messages.error(request,'product not found')