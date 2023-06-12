from django.urls import path 
from . import views
from store.controller import authview,cart, order,wishlist,checkout,reviews

urlpatterns = [
    path('',views.home,name='home'),
    path("collections/", views.collections,name='collections'),
    path("collections/<str:slug>",views.collectionsView, name="collectionsView"),
    path("collections/<str:cate_slug>/<str:prod_slug>",views.productView, name="productView"),
    
    path("product-list/", views.productListAjax),
    path("search-products/", views.searchProduct,name="searchProduct"),
    
    path('register/',authview.register,name='register'),
    path('login/',authview.loginpage,name='loginpage'),
    path('logout/',authview.logoutpage,name='logoutpage'),
    
    
    path("cart/",cart.viewCart,name='viewCart'),
    path('add-to-cart/',cart.addToCart,name='addToCart'),
    path('update-cart/',cart.updateCart,name='updateCart'),
    path('delete-cart/',cart.deleteCartItem,name='deleteCartItem'),
    path('wishlist/',wishlist.viewWishList,name='viewWishList'),
    path('add-to-wishlist/<int:product_id>/',wishlist.addToWishList,name='addToWishList'),
    path('delete-item-wishlist/<int:product_id>/',wishlist.deleteWishlistItem,name='deleteWishlistItem'),
    
    path('checkout/',checkout.viewCheckout,name='checkout'),
    path('place-order',checkout.placeorder,name='placeorder'),
    
    path("proceed-to-pay",checkout.razorPaycheck),
    path("my-orders/",order.viewOrderList,name='myorders'),
    path("my-orders/<str:t_no>",order.viewOrder,name='orderView'),
    
    
    path("post-review/<str:p_id>",reviews.postReview,name='postReview'),
]
