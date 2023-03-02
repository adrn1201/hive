from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from wholesalers.models import Wholesaler, Domain
from django_tenants.utils import remove_www


def paginate_orders(request, orders, results):
    page = request.GET.get('page')
    paginator = Paginator(orders, results)
    
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


def search_orders(request):
    search_query = ''
    order_query = ''

    if request.GET.get('q'):
        search_query = request.GET.get('q')
        
    if request.GET.get('category'):
        order_query = request.GET.get('category')
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    
    order_filter = wholesaler.order_set.filter(status__icontains=order_query)

    orders = wholesaler.order_set.distinct().filter(Q(id__in=order_filter) &(Q(business_name__icontains=search_query) | 
                                                    Q(mode_of_payment__icontains=search_query) |
                                                    Q(status__icontains=search_query)))

    return orders, search_query


import random
import string


def random_string_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_order_id_generator(instance):
    reference_number= random_string_generator()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(reference_number=reference_number).exists()
    if qs_exists:   
        return unique_order_id_generator(instance)
    return reference_number