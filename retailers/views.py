from django.shortcuts import render, redirect
from django_tenants.utils import remove_www
from django.contrib.auth import login, authenticate, logout
<<<<<<< Updated upstream
=======
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
>>>>>>> Stashed changes
from wholesalers.models import Wholesaler
from django.conf import settings
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
    return render(request, 'retailers/retailers_profile.html', context)


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
<<<<<<< Updated upstream
    return render(request, "retailers/retailers.html", context)
=======

    if(request.method == "POST"):
        send_mail(
            'Hive Account Registration',
            f'Please click the link to register your account http://{hostname_without_port}:8000/retailers/register',
            settings.EMAIL_HOST_USER,
            [request.POST['email']],
            fail_silently=False
        )
        return redirect('retailers')
    return render(request, "retailers/retailers.html", context)


@login_required(login_url='login_retailer')
def dashboard_retailer(request):
    orders = request.user.order_set.all()   
    context = {'orders': orders}
    return render(request, "retailers/dashboard.html", context)
>>>>>>> Stashed changes
