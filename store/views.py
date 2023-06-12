from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.db.models import Q
from django.contrib import messages
# Create your views here.
class PriceRange():
    def __init__(self,name,min,max):
        self.name = name
        self.min = min
        self.max = max


priceRanges = [
            PriceRange("0-1000",0,1000),
            PriceRange("1000-5000",1000,5000),
            PriceRange("5000-10000",5000,10000),
            PriceRange("10000-20000",10000,20000),
            PriceRange("20000-more",20000,None),
        ]

def home(request):
    trending_products = Product.objects.filter(trending=1)[:4]
    bestseller_products = Product.objects.filter(Q(main_tag='bestseller') | Q(tags__name__in=['bestseller'])).order_by('-created_at').distinct()[:4]
    hot_products = Product.objects.filter(Q(main_tag='Hot') | Q(tags__name__in=['Hot'])).order_by('-created_at').distinct()[:4]
    new_products = Product.objects.filter(Q(main_tag='New') | Q(tags__name__in=['New'])).order_by('-created_at').distinct()[:4]
    
    context = {
        'trending_products':trending_products,
        'bestseller_products':bestseller_products,
        'hot_products':hot_products,
        'new_products':new_products,
    }
    return render(request, 'store/index.html',context)

def collections(request):
    category = Category.objects.filter(status=0)
    context = {'category': category}
    return render(request, 'store/categorycollections.html',context)

# def collectionsView(request,slug):
#     if(Category.objects.filter(slug=slug,status=0)):
#         products = Product.objects.filter(category__slug=slug)
#         category_name = Category.objects.filter(slug=slug).first()
#         context = {'products':products,'category_name':category_name}
#         return render(request,'store/products/index.html',context)
#     else:
#         messages.warning(request,"No such category found")
#         return redirect('collections')

def collectionsView(request, slug):
    if Category.objects.filter(slug=slug, status=0):
        
        products = Product.objects.filter(category__slug=slug)
        brands = Brand.objects.all()

        if request.method == 'POST':
            # Apply filters based on user-selected options
            price_filter = request.POST.get('price_filter')
            

            nonecount=0
            
            brand_filters = request.POST.getlist('brand_filter')
            
            sort_by = request.POST.get('sort_by')
            if price_filter is None and sort_by is None and brand_filters is None:
                messages.error(request,"Select a filter first")

            if price_filter:
                # Apply price filter logic based on the selected price range
                # Modify the queryset 'products' accordingly
                min_price, max_price = price_filter.split('-')
            
                
                # Filter products based on the selling price range
                if max_price == 'more':
                    products = products.filter(selling_price__gte=min_price)
                else:
                    products = products.filter(selling_price__range=(min_price, max_price))
            else:
                nonecount+=1

            if brand_filters:
                # messages.success(request,brand_filter)
                products = products.filter(tags__name__in=brand_filters)
            else:
                nonecount+=1
                # Apply brand filter logic based on the selected brands
                # Modify the queryset 'products' accordingly
                
                

            if sort_by == 'price-high':
                products = products.order_by('-selling_price')
            elif sort_by == 'price-low':
                products = products.order_by('selling_price')
            elif sort_by == 'ratings':
                products = products.order_by('-average_rating')
            elif sort_by == 'new_arrival':
                products = products.order_by('-id')
            else:
                nonecount+=1
                # Apply sorting logic based on ratings
                # Modify the queryset 'products' accordingly
            # if nonecount == 3:
            #     messages.warning(request, "You have not selected any filters")
            
        category_name = Category.objects.filter(slug=slug).first()
        
        context = {
            'products': products,
            'category_name': category_name,
            'brands': brands,
            'priceRanges': priceRanges,
        }
        return render(request, 'store/products/index.html', context)
    else:
        messages.warning(request, "No such category found")
        return redirect('collections')
   

def productView(request,cate_slug,prod_slug):
    if(Category.objects.filter(slug=cate_slug,status=0)):
        if(Product.objects.filter(slug=prod_slug,status=0)):
            product = Product.objects.filter(slug=prod_slug,status=0).first()
            reviews = Rating.objects.filter(product=product).all().order_by('-created_at')
            discount_percentage = ((product.original_price - product.selling_price) / product.original_price) * 100
            context = {
                'product':product,
                'title':(str)(product.name),
                'reviews':reviews,
                'discount_percentage':discount_percentage
            }
        else:
            messages.warning(request,"No such product found")
            return redirect('collections')
    else:
        messages.error(request,"No such category found")
        return redirect('collections')
    
    return render(request,'store/products/productView.html',context)

def productListAjax(request):
    products = Product.objects.filter(status=0).values_list('name',flat=True)
    productList = list(products)
    
    return JsonResponse(productList,safe=False)


def searchProduct(request):
    # if request.method == 'POST':
    #     searchedTerm = (str)(request.POST.get('product-search'))
    #     if searchedTerm=="":
    #         messages.info(request, "Product not found")
    #         return redirect(request.META.get('HTTP_REFERER', '/'))
    #     else:
            
    #         product = Product.objects.filter(name__icontains=searchedTerm).first()
    #         if product:
    #             return redirect('/collections/'+product.category.slug)
    #         else:
    #             messages.info(request, "Product not found")
    #             return redirect(request.META.get('HTTP_REFERER'))
    # else:
    #     return redirect(request.META.get('HTTP_REFERER'))
    product_search = request.GET.get('product-search') 
    if request.GET.get('product-search') != None:
        products = Product.objects.filter(
            Q(name__icontains=product_search) |
            Q(tags__name__icontains=product_search) |
            Q(meta_keywords__icontains=product_search)
        ).distinct()
        
    products = products.distinct()
    context={
        'products': products,
    }
    return render(request, 'store/products/productlist.html',context)