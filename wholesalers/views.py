from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, WholesalerCreationForm
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from .models import Domain



def register_wholesalers(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('profile_wholesalers')

        else:
          pass
    context = {'form':form}
    return render(request, "wholesalers/create_wholesalers.html", context)


def wholesaler_profile(request):
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
            domain.tenant = wholesaler
            domain.is_primary = True
            domain.save()
            
            return redirect('products')

    context = {'form':form}
    return render(request, 'wholesalers/wholesaler_profile.html', context)
    
    



