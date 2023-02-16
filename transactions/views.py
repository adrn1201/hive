from django.shortcuts import render
from django.http import HttpResponseForbidden
from django_tenants.utils import remove_www
from wholesalers.models import Domain, Wholesaler
from django.contrib.auth.decorators import login_required


@login_required(login_url='login_wholesaler')
def display_transactions(request):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
   
    completed_orders = wholesaler.order_set.filter(status='completed')
    context = {'completed_orders':completed_orders}
    
    return render(request, "transactions/transactions.html", context)
