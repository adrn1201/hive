from django.shortcuts import render
from products.models import Product
from django_tenants.utils import remove_www
from wholesalers.models import Domain, Wholesaler
from django.contrib.auth.decorators import login_required
from products.utils import search_products, paginate_products


@login_required(login_url='login_retailer')
def show_shop(request):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    
    categories = wholesaler.category_set.all()
    products, search_query = search_products(request)
    custom_range, products = paginate_products(request, products, 9)
    context = {'categories':categories, 'products': products, 'search_query': search_query, 'custom_range':custom_range}
    return render(request, "shop/shop.html", context)

@login_required(login_url='login_retailer')
def view_item (request,pk):
    item = Product.objects.get(id=pk)
    sizes = item.variation_set.all()
    context ={'item':item, 'sizes':sizes}
    return render(request, "shop/item_view.html", context)