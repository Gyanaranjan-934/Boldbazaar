from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import Order,OrderItem
from django.contrib.auth.models import User

@login_required(login_url='loginpage')    
def viewOrderList(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders':orders,'title':"My Orders"}
    return render(request,'store/orders/my-orders.html', context)

def viewOrder(request,t_no):
    order = Order.objects.filter(tracking_no = t_no).filter(user=request.user).first()
    orderItems = OrderItem.objects.filter(order=order)
    context = {
        'orderItems': orderItems,
        'order': order,
        'title': t_no,
    }
    return render(request,'store/orders/order-view.html',context)