from django.contrib import admin

from store.models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)
admin.site.register(Rating)
admin.site.register(Tag)
admin.site.register(Brand)