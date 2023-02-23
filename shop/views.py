from django.shortcuts import render
from products.models import Inventory
from django.contrib.auth.decorators import login_required
from products.utils import search_products, paginate_products


@login_required(login_url='login_retailer')
def show_shop(request):
    products, search_query = search_products(request)
    custom_range, products = paginate_products(request, products, 10)
    context = {'products': products, 'search_query': search_query, 'custom_range':custom_range}
    return render(request, "shop/shop.html", context)

@login_required(login_url='login_retailer')
def view_item (request,pk):
    item = Inventory.objects.get(id=pk)

    context ={'item':item}
    return render(request, "shop/item_view.html", context)