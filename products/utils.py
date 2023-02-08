from django.db.models import Q
from products.models import Inventory, Category



def search_products(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    categories = Category.objects.filter(name__icontains=search_query)

    products = Inventory.objects.distinct().filter(Q(product_name__icontains=search_query) | Q(category__in=categories))

    return products, search_query