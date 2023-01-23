from django.shortcuts import render
from products.models import Inventory
from .utils import search_products, paginate_products

def show_shop(request):
    products, search_query = search_products(request)
    custom_range, products = paginate_products(request, products, 1)
    context = {'products': products, 'search_query': search_query, 'custom_range':custom_range}
    return render(request, "shop/shop.html", context)
