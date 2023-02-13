from django.shortcuts import render, redirect
from django_tenants.utils import remove_www
from django.contrib.auth import login, authenticate, logout
from wholesalers.models import Wholesaler
from wholesalers.models import Domain
from .models import Retailer
from .forms import RetailerCreationForm, CustomUserCreationForm


def register_retailer(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('retailer_create_profile')

        else:
          pass
    context = {'form':form}
    return render(request, "retailers/create_retailer.html", context)


def retailer_create_profile(request):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    form = RetailerCreationForm()
    
    if request.method == "POST":
        form = RetailerCreationForm(request.POST)
        if form.is_valid():
            retailer = form.save(commit=False)
            retailer.user = request.user
            retailer.wholesaler = Wholesaler.objects.get(id=wholesaler_id)
            retailer.is_active = True
            retailer.save()
            return redirect('show_shop')

    context = {'form':form}
    return render(request, 'retailers/retailer_create_profile.html', context)


def retailer_edit_profile(request):
    retailer = request.user.retailer
    form = RetailerCreationForm(instance=retailer)
    if request.method == "POST":
        form = RetailerCreationForm(request.POST, instance=retailer)
        if form.is_valid():
            form.save()
            return redirect('retailer_edit_profile')


    context = {'form':form}
    return render(request, 'wholesalers/wholesaler_profile.html', context)


def index(request):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    retailers = Retailer.objects.filter(wholesaler=wholesaler_id)
    context = {'retailers':retailers}
    return render(request, "retailers/retailers.html", context)