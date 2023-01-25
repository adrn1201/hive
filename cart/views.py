from django.shortcuts import render
from products.models import Inventory


def show_cart(request):
    return render(request, "cart/shop_cart.html")



   