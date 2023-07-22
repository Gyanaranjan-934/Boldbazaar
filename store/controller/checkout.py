from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import Cart,Order,OrderItem, Product,Profile
from django.contrib.auth.models import User

import random

@login_required(login_url='loginpage')
def viewCheckout(request):
    rawCart = Cart.objects.filter(user=request.user)
    cartitems = []
    total_price = 0
    
    for item in rawCart:
        if item.product_qty <= item.product.quantity:
            cartitems.append(item)
            total_price += item.product_qty * item.product.selling_price
    
    if len(cartitems)==0:
        messages.error(request,'Nothing to take to cart')
        return redirect('viewCart')
    
    userProfile = Profile.objects.filter(user=request.user).first()
    
    
    context = {
        'cartitems': cartitems,
        'total_price': total_price,
        'userprofile': userProfile,
    }
    
    return render(request, 'store/checkout.html', context)

@login_required(login_url='loginpage')
def placeorder(request):
    if request.method == 'POST':
        
        currentUser = User.objects.filter(id=request.user.id).first()
        
        if not currentUser.first_name:
            currentUser.first_name = request.POST.get('firstname')
            currentUser.last_name = request.POST.get('lastname')
            currentUser.save()
        
        if not Profile.objects.filter(user=currentUser):
            userProfile = Profile()
            userProfile.user = request.user
            phoneNo = (str)(request.POST.get('phone'))
            if not phoneNo.isdigit() or (len)(phoneNo) >10 or (len)(phoneNo) < 10:
                messages.error(request, 'Invalid phone number')
                return redirect('checkout')    
            userProfile.phone = request.POST.get('phone')
            userProfile.address = request.POST.get('address')
            userProfile.city = request.POST.get('city')
            userProfile.state = request.POST.get('state')
            userProfile.country = request.POST.get('country')
            userProfile.pincode = request.POST.get('pincode')
            userProfile.save()
        
        newOrder = Order()
        newOrder.user = request.user
        newOrder.fname = request.POST.get('firstname')
        newOrder.lname = request.POST.get('lastname')
        newOrder.email = request.POST.get('email')
        phoneNo = (str)(request.POST.get('phone'))
        if not phoneNo.isdigit() or (len)(phoneNo) >10 or (len)(phoneNo) < 10:
            messages.error(request, 'Invalid phone number')
            return redirect('checkout')    
        newOrder.phone = request.POST.get('phone')
        newOrder.address = request.POST.get('address')
        newOrder.city = request.POST.get('city')
        newOrder.state = request.POST.get('state')
        newOrder.country = request.POST.get('country')
        newOrder.pincode = request.POST.get('pincode')
        
        newOrder.payment_mode = request.POST.get('payment_mode')
        newOrder.payment_id = request.POST.get('payment_id')
        
    
        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price += (item.product.selling_price*item.product_qty)
        
        newOrder.total_price = cart_total_price
        fname = (str)(request.user.username)
        track_no = fname[0:3]+str(random.randint(1111111,9999999))+phoneNo[5:10]
        while Order.objects.filter(tracking_no=track_no) is None:
            track_no = fname[0:3]+str(random.randint(1111111,9999999))+phoneNo[5:10]
        newOrder.tracking_no = track_no
        newOrder.save()
        
        newOrderItems = Cart.objects.filter(user=request.user)
        for item in newOrderItems:
            OrderItem.objects.create(
                order=newOrder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )
            
            # to decrease or reduce the product quantity from available stock
            orderProduct = Product.objects.filter(id=item.product_id).first()
            orderProduct.quantity -= item.product_qty
            orderProduct.save()
            
        # to clear cart
        Cart.objects.filter(user=request.user).delete() 
        
        messages.success(request,'Your order has been placed successfully')
        
        paymode = request.POST.get('payment_mode')
        if paymode == 'Razorpay':
            return JsonResponse({'status':'Your order has been placed successfully\n Please go to order section for order details'})
    return redirect('home')

def viewOrders(request):
    pass

def razorPaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price += (item.product_qty * item.product.selling_price)
    
    return JsonResponse({
        'total_price': total_price,
    })



    