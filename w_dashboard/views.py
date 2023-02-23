from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django_tenants.utils import remove_www
from wholesalers.models import Domain, Wholesaler

@login_required(login_url='login_wholesaler')
def w_dashboard(request):    
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    products = wholesaler.product_set.all()
    categories = wholesaler.category_set.all()
    
    pending = wholesaler.order_set.filter(status='pending').count()
    preparing = wholesaler.order_set.filter(status='preparing').count()
    shipped = wholesaler.order_set.filter(status='shipped').count()
    completed = wholesaler.order_set.filter(status='completed').count()
    orders = wholesaler.order_set.all().order_by('-created')
    products_stock_level = wholesaler.product_set.filter(actual_stocks__lte='15')
    context = {
        'products':products, 
        'categories':categories,
        'pending' :pending,
        'preparing': preparing,
        'shipped':shipped,
        'completed':completed,
        'orders':orders,
        'products_stock_level':products_stock_level
    }
    return render(request, 'w_dashboard/dashboard.html', context)
