from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from wholesalers.models import Wholesaler
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .utils import login_user, logout_user, search_products

@login_required(login_url='login_admin')
def register_admin(request):

    if request.user.is_authenticated and request.user.is_superuser:
        pass
    elif request.user.is_authenticated and not request.user.is_superuser:
        return redirect('login_admin')
    
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.is_superuser = True
            user.is_staff = True
            user.save()
            global user_credentials
            user_credentials = user
            return redirect('register_admin')
        else:
            pass
        

    context = {'form': form}

    return render(request, "hiveadmin/create_admin.html", context)

def login_admin(request):
    '''
    This function is for wholesaler account authentication
    '''

    return login_user(request, 'list_wholesalers', 'hiveadmin/admin_login.html')


@login_required(login_url='login_admin')
def logout_admin(request):
    return logout_user(request, 'login_admin')

@login_required(login_url='login_admin')
def dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        pass
    elif request.user.is_authenticated and not request.user.is_superuser:
        return redirect('login_admin')
    
    return render(request, 'hiveadmin/dashboard.html')

@login_required(login_url='login_admin')
def list_wholesalers(request):

    if request.user.is_authenticated and request.user.is_superuser:
        pass
    elif request.user.is_authenticated and not request.user.is_superuser:
        return redirect('login_admin')
    
    wholesalers = Wholesaler.objects.exclude(id=1).filter(is_active=True)
    context = {'wholesalers': wholesalers}

    if(request.method == "POST"):
        send_mail(
            'Hive Account Registration',
            'Please click the link to register your account http://localhost:8000/wholesalers/register',
            settings.EMAIL_HOST_USER,
            [request.POST['email']],
            fail_silently=False
        )
        messages.success(request, 'Registration has been successfully sent!')
        return redirect('list_wholesalers')
    return render(request, 'hiveadmin/wholesalers_list.html',context)

@login_required(login_url='login_admin')
def transactions(request):
    if request.user.is_authenticated and request.user.is_superuser:
        pass
    elif request.user.is_authenticated and not request.user.is_superuser:
        return redirect('login_admin')
    return render(request, 'hiveadmin/transactions.html')

@login_required(login_url='login_admin')
def admins(request):
    if request.user.is_authenticated and request.user.is_superuser:
        pass
    elif request.user.is_authenticated and not request.user.is_superuser:
        return redirect('login_admin')
    return render(request, 'hiveadmin/list_admin.html')

@login_required(login_url='login_admin')
def registration_logs (request):
    if request.user.is_authenticated and request.user.is_superuser:
        pass
    elif request.user.is_authenticated and not request.user.is_superuser:
        return redirect('login_admin')
    return render(request, 'hiveadmin/logs.html')

@login_required(login_url='login_admin')
def update_wholesaler(request, pk):

    if request.user.is_authenticated and request.user.is_superuser:
        pass
    elif request.user.is_authenticated and not request.user.is_superuser:
        return redirect('login_admin')
    
    wholesaler = Wholesaler.objects.get(id=pk)
    
    
    if request.method == "POST":
    
        if wholesaler.is_active & wholesaler.user.is_active == False:
            wholesaler.is_active = True
            wholesaler.user.is_active = True
            wholesaler.user.save()
            wholesaler.save()
            
        
        elif wholesaler.is_active & wholesaler.user.is_active == True:
            wholesaler.is_active = False
            wholesaler.user.is_active = False
            wholesaler.user.save()
            wholesaler.save()


        messages.success(request, 'Account status successfully updated!') 
        return redirect('list_wholesalers')
    context = {"wholesaler":wholesaler}
    return render(request, 'hiveadmin/wholesalers_list.html',context)
        

      
