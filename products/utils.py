from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from wholesalers.models import Wholesaler, Domain
from django_tenants.utils import remove_www


def paginate_products(request, products, results):
    page = request.GET.get('page')
    paginator = Paginator(products, results)
    
    try:
        products = paginator.page(page)  
    except PageNotAnInteger:
        page = 1 
        products = paginator.page(page)  
    except EmptyPage:
        page = paginator.num_pages 
        products = paginator.page(page)  
        
    left_index = (int(page) - 4)
    
    if left_index < 1:
        left_index = 1
        
    right_index = (int(page) + 5)
    
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
    
    custom_range = range(left_index, right_index)
    return custom_range, products


def search_products(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    
    categories = wholesaler.category_set.filter(name__icontains=search_query)

    products = wholesaler.inventory_set.distinct().filter(Q(product_name__icontains=search_query) | Q(category__in=categories))

    return products, search_query

