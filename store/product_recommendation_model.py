import pandas as pd
import numpy as np
from .models import *


def createDataFrame(products):
    pass

def get_products_from_model(user_id):
    user = User.objects.get(id=user_id)

    wishlist_products_ids = Wishlist.objects.filter(user=user).values_list('product', flat=True)
    cart_product_ids = Cart.objects.filter(user=user).values_list('product', flat=True)
    orders_ids = Order.objects.filter(user=user)
    ordered_product_ids = OrderItem.objects.filter(order__in=orders_ids).values_list('product', flat=True)

    product_ids = wishlist_products_ids.union(cart_product_ids, ordered_product_ids)
    distinct_products = Product.objects.filter(id__in=product_ids)

    df = createDataFrame(distinct_products)
    
    