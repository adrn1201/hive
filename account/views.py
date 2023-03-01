from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from wholesalers.models import Domain, Wholesaler
from django_tenants.utils import remove_www
from django.contrib.auth.decorators import login_required
from .utils import login_user, logout_user


def login_wholesaler(request):
    '''
    This function is for wholesaler account authentication
    '''
    try:
        if request.user.is_authenticated and request.user.wholesaler:
            
            
            return redirect('w_dashboard')
    except:
        
        return HttpResponseForbidden()

    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    print(wholesaler.color)
    context = {'wholesaler': wholesaler}

    return login_user(request, 'w_dashboard', 'account/wholesaler_login.html', context)


@login_required(login_url='login_wholesaler')
def logout_wholesaler(request):
    '''
    This function is for wholesaler account logout
    '''
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    return logout_user(request, 'login_wholesaler')



def login_retailer(request):
    '''
    This function is for retailer account authentication
    '''
    try:
        if request.user.is_authenticated and request.user.retailer:
            return redirect('shop_shop')
    except:
        return HttpResponseForbidden()
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    
    context = {'wholesaler': wholesaler}

    return login_user(request, 'show_shop', 'account/retailer_login.html', context)


@login_required(login_url='login_retailer')
def logout_retailer(request):
    '''
    This function is for retailer account logout
    '''
    try:
        request.user.retailer
    except:
        return HttpResponseForbidden()
    return logout_user(request, 'login_retailer')