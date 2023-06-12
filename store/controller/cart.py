from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import *

def addToCart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = (int)(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Cart.objects.filter(user=request.user,product_id=prod_id)):
                    messages.warning(request,'Product already in cart')
                    
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user, product_id=prod_id,product_qty=prod_qty)
                        messages.success(request, 'Product added successfully')
                        return redirect('viewCart')
                    else:
                        messages.warning(request, f'Only {product_check.quantity} quantity available')
            else:
                messages.error(request, 'No such product found')
        else:
            messages.error(request, 'Login to Continue')
            return redirect('loginpage')
    return redirect(request.META.get('HTTP_REFERER'))
    
from django.core.exceptions import ObjectDoesNotExist
@login_required(login_url='loginpage')
def viewCart(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    context = {'cart': cart,'title':"Shopping Cart | BoldBazaar"}
    return render(request, 'store/cartView.html', context)

def updateCart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = request.POST.get('prod_id')
            if prod_id is None:
                messages.error(request, "No such product found")
            else:
                prod_id = (int(prod_id))
                product_check = Product.objects.get(id=prod_id)
                if product_check:
                    prod_qty = int(request.POST.get('product_qty'))
                    if prod_qty > product_check.quantity:
                        messages.warning(request, f"Only {product_check.quantity} quantity available")
                    else:
                        cart_item = Cart.objects.get(user=request.user, product_id=prod_id)
                        cart_item.product_qty = prod_qty
                        cart_item.save()
                        
                else:
                    messages.error(request, "No such product found")
        else:
            messages.error(request, "Login to continue")
    return redirect('viewCart')



def deleteCartItem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('prod_id'))
            try:
                cart_item = Cart.objects.get(user_id=request.user.id, product_id=prod_id)
                cart_item.delete()
                messages.success(request, "Item deleted")
            except ObjectDoesNotExist:
                messages.error(request, "Cart item does not exist")
        else:
            messages.error(request, "Login to continue")
            return redirect('loginpage')
    return redirect('viewCart')
