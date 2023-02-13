from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, WholesalerCreationForm
from django.core.exceptions import ValidationError  
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from .models import Domain, Wholesaler
from django_tenants.utils import remove_www


def register_wholesalers(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('wholesaler_create_profile')

        else:
          pass
    context = {'form':form}
    return render(request, "wholesalers/create_wholesalers.html", context)


def wholesaler_create_profile(request):
    form = WholesalerCreationForm()
    if request.method == "POST":
        form = WholesalerCreationForm(request.POST)
        if form.is_valid():
            wholesaler = form.save(commit=False)
            wholesaler.user = request.user
            wholesaler.schema_name = wholesaler.business_name.lower()
            wholesaler.is_active = True
            
            wholesaler.save()

            domain = Domain()
            domain.domain = str(wholesaler.business_name.replace(' ', '-').lower())+'.localhost'
            redirect_url = domain.domain
            domain.tenant = wholesaler
            domain.is_primary = True
            domain.save()
            
            return redirect(f'http://{redirect_url}:8000')

    context = {'form':form}
    return render(request, 'wholesalers/wholesaler_profile.html', context)


def wholesaler_edit_profile(request):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    form = WholesalerCreationForm(instance=wholesaler)
    if request.method == "POST":
        form = WholesalerCreationForm(request.POST, instance=wholesaler)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')


    context = {'form':form}
    return render(request, 'wholesalers/wholesaler_profile.html', context)


def email_retailer(request):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    if(request.method == "POST"):
        send_mail(
            'Hive Account Registration',
            f'Please click the link to register your account http://{hostname_without_port}:8000/retailers/register',
            settings.EMAIL_HOST_USER,
            [request.POST['email']],
            fail_silently=False  
        )
        return redirect('retailers')
    return render(request, 'wholesalers/email_retailer.html')
    
    



