from django.shortcuts import render
from products.models import Product
from django.contrib.auth.decorators import login_required
from products.utils import search_products, paginate_products


@login_required(login_url='login_retailer')
def show_shop(request):
    products, search_query = search_products(request)
    custom_range, products = paginate_products(request, products, 1)
    context = {'products': products, 'search_query': search_query, 'custom_range':custom_range}
    return render(request, "shop/shop.html", context)

@login_required(login_url='login_retailer')
def view_item (request,pk):
    item = Product.objects.get(id=pk)
    sizes = item.variation_set.all()
    context ={'item':item, 'sizes':sizes}
    return render(request, "shop/item_view.html", context)