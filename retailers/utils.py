from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from wholesalers.models import Wholesaler, Domain
from django_tenants.utils import remove_www
from retailers.models import RetailerLogs  


def paginate_retailers(request, retailers, results):
    page = request.GET.get('page')
    paginator = Paginator(retailers, results)
    
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


def search_retailers(request):
    search_query = ''
    retailer_query = ''

    if request.GET.get('q'):
        search_query = request.GET.get('q')
        
    if request.GET.get('category'):
        retailer_query = request.GET.get('category')
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    
    retailer_filter = wholesaler.retailers.filter(is_active__icontains=retailer_query)

    retailers = wholesaler.retailers.distinct().filter(Q(id__in=retailer_filter) &(Q(business_name__icontains=search_query) | 
                                                    Q(contact_name__icontains=search_query) |
                                                    Q(address__icontains=search_query)))

    return retailers, search_query

def search_retailers_log(request):
    search_query = ''
    retailer_query = ''

    if request.GET.get('q'):
        search_query = request.GET.get('q')
        
    if request.GET.get('category'):
        retailer_query = request.GET.get('category')
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    
    retailers_all = RetailerLogs.objects.filter(Q(retailer__icontains=search_query))

    return retailers_all, search_query

