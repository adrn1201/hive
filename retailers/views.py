from django.shortcuts import render, redirect
from django_tenants.utils import remove_www
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from wholesalers.models import Wholesaler
from wholesalers.models import Domain
from .models import Retailer
from .forms import RetailerCreationForm, CustomUserCreationForm

user_credentials = ''

def register_retailer(request):
    try:
        if request.user.is_authenticated and request.user.retailer:
            return redirect('show_shop')
    except:
        return HttpResponseForbidden()
    
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            global user_credentials
            user_credentials = user
            return redirect('retailer_create_profile')

        else:
          pass
    context = {'form':form}
    return render(request, "retailers/create_retailer.html", context)


def retailer_create_profile(request):
    try:
        if request.user.is_authenticated and request.user.retailer:
            return redirect('show_shop')
    except:
        return HttpResponseForbidden()
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    form = RetailerCreationForm()
    
    if request.method == "POST":
        form = RetailerCreationForm(request.POST)
        if form.is_valid():
            retailer = form.save(commit=False)
            user_credentials.save()
            retailer.user = user_credentials    
            retailer.wholesaler = Wholesaler.objects.get(id=wholesaler_id)
            retailer.is_active = True
            retailer.save()
            login(request, user_credentials)
            return redirect('show_shop')

    context = {'form':form}
    return render(request, 'retailers/retailers_profile.html', context)


@login_required(login_url='login_wholesaler')
def retailer_edit_profile(request):
    try:
        request.user.retailer
    except:
        return HttpResponseForbidden()
    retailer = request.user.retailer
    form = RetailerCreationForm(instance=retailer)
    if request.method == "POST":
        form = RetailerCreationForm(request.POST, instance=retailer)
        if form.is_valid():
            form.save()
            return redirect('retailer_edit_profile')


    context = {'form':form}
    return render(request, 'retailers/retailer_edit_profile.html', context)


@login_required(login_url='login_wholesaler')
def index(request):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    retailers = Retailer.objects.filter(wholesaler=wholesaler_id)
    context = {'retailers':retailers}
    return render(request, "retailers/retailers.html", context)