from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from store.models import *
from django.db.models import Avg
from django.contrib.auth.decorators import login_required


def update_average_rating(product):
    reviews = Rating.objects.filter(product=product, rating__isnull=False)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    product.average_rating = average_rating
    product.save()


def postReview(request,p_id):
    if request.method == 'POST' and request.user.is_authenticated:
        rating  = request.POST.get('rating')
        reviewText = request.POST.get('review')
        product = Product.objects.get(id=p_id)
        if product:
            order = Order.objects.filter(user=request.user, orderitem__product_id=product.id).first()
            if order:
                Rating.objects.create(user=request.user, product=product, rating=rating,review=reviewText)
                update_average_rating(product)
                messages.success(request,'Thank you for your feedback')
            else:
                messages.warning(request,'You have not purchased the product yet!')
            url = reverse('productView', args=[product.category.slug, product.slug])
            return redirect(url)
        else:
            messages.warning(request,'Product not found')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request,'You are not logged in')
        return redirect('loginpage')



            
        
        