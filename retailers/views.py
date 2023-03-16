from django.shortcuts import render, redirect, get_object_or_404
from django_tenants.utils import remove_www
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from wholesalers.models import Wholesaler
from retailers.models import Retailer, RetailerLogs  
from django.conf import settings
from wholesalers.models import Domain
from .models import Retailer
from orders.models import Order, OrderItem
from .forms import RetailerCreationForm, CustomUserCreationForm
from django.contrib import messages
from .utils import search_retailers, paginate_retailers, search_retailers_log, paginate_myOrders
from hiveadmin.models import AdminWholesalerLogs,AdminRetailerLogs
from django_tenants.utils import remove_www
from wholesalers.models import Domain
from wholesalers.models import Wholesaler
from django.urls import reverse
from django.http import HttpResponseRedirect


user_credentials = ''


def register_retailer(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.is_retailer = True
            global user_credentials
            user_credentials = user
            return redirect('retailer_create_profile')

        else:
            pass

    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    print(wholesaler.color)

    context = {'form': form, 'wholesaler': wholesaler}
    return render(request, "retailers/create_retailer.html", context)


def retailer_create_profile(request):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    form = RetailerCreationForm()
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    print(wholesaler.color)

    if request.method == "POST":
        form = RetailerCreationForm(request.POST, request.FILES)
        if form.is_valid():
            retailer = form.save(commit=False)
            user_credentials.save()
            retailer.user = user_credentials
            retailer.wholesaler = Wholesaler.objects.get(id=wholesaler_id)
            retailer.is_active = True
            retailer.save()
            
            login(request, user_credentials)
            return redirect('show_shop')

    context = {'form': form, 'wholesaler': wholesaler}
    return render(request, 'retailers/retailers_profile.html', context)


@login_required(login_url='login_wholesaler')
def retailer_edit_profile(request):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)

    retailer = request.user.retailer
    form = RetailerCreationForm(instance=retailer)
    if request.method == "POST":
        form = RetailerCreationForm(request.POST, request.FILES, instance=retailer)
        if form.is_valid():
            form.save()
            RetailerLogs.objects.create(
                retailer=retailer.business_name,
                action = 'Updated profile',
            )             
            AdminRetailerLogs.objects.create(
                wholesaler = wholesaler.business_name,
                retailer = retailer.business_name,
                domain = domain,
                action = 'Updated Profile'
            )
            return redirect('retailer_view_profile')
        


    context = {'form': form}
    return render(request, 'retailers/retailer_edit_profile.html', context)

@login_required(login_url='login_wholesaler')
def retailer_view_profile(request):
    try:
        retailer = request.user.retailer
    except:
        return redirect('show_shop')
    context ={'retailer':retailer}
    return render(request, "retailers/retailer_view_profile.html", context)

# IN PROGRESS IN PROGRESS IN PROGRESS IN PROGRESS  IN PROGRESS IN PROGRESS 

@login_required(login_url='login_wholesaler')
def about_us(request):    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    context ={'wholesaler':wholesaler}
    
    if request.method == 'POST':
        subject = request.POST["subject"]
        message = request.POST['message']
        sender = request.POST['email']
        name = request.POST['name']
        send_mail(
            f'{subject}',
            f'{name} {sender} {message}',
            sender,
            [request.user.retailer.wholesaler.user.email],
            fail_silently=False
        )
        messages.success(request, 'Message Sent!')
        return redirect('about_us')
        
       
    return render(request, "retailers/about_us.html",context)

# IN PROGRESS IN PROGRESS IN PROGRESS IN PROGRESS  IN PROGRESS IN PROGRESS 

@login_required(login_url='login_wholesaler')
def index(request):    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    retailers, search_query = search_retailers(request)
    custom_range, retailers = paginate_retailers(request, retailers, 10)
    
    context = {'retailers':retailers, 'custom_range':custom_range, 'search_query':search_query}

    if(request.method == "POST"):
        send_mail(
            'Hive Account Registration',
            f'Please click the link to register your account http://{domain.domain}:8000/retailers/register',
            settings.EMAIL_HOST_USER,
            [request.POST['email']],
            fail_silently=False
        )
            
        email_data = request.POST["email"]
        AdminWholesalerLogs.objects.create(
            wholesaler = wholesaler.business_name,
            domain = domain,
            action = f'Sent Registration Email to {email_data}'
        )
        messages.success(request, 'Registration has been successfully sent!')
        return redirect('retailers')             
    return render(request, "retailers/retailers.html", context)

@login_required(login_url='login_retailer')
def dashboard_retailer(request):

    order_status = request.GET.get('status')
    if order_status:
        orders = request.user.order_set.distinct().filter(status=order_status)
    else:
        orders = request.user.order_set.all()
     
    pending_count = request.user.order_set.distinct().filter(status="pending").count()
    preparing_count = request.user.order_set.distinct().filter(status="preparing").count()
    shipped_count = request.user.order_set.distinct().filter(status="shipped").count()
    completed_count = request.user.order_set.distinct().filter(status="completed").count()

    custom_range, orders = paginate_myOrders(request, orders, 10)

    context = {
        'orders': orders,
        'pending': pending_count,
        'preparing': preparing_count,
        'shipped': shipped_count,
        'completed': completed_count,
        'custom_range': custom_range, 
    }
    
    return render(request, "retailers/dashboard.html", context)


@login_required(login_url='login_retailer')
def order_items(request, pk):
    order = Order.objects.get(id=pk)
    order_items = order.items.all()

    pending_count = request.user.order_set.distinct().filter(status="pending").count()
    preparing_count = request.user.order_set.distinct().filter(status="preparing").count()
    shipped_count = request.user.order_set.distinct().filter(status="shipped").count()
    completed_count = request.user.order_set.distinct().filter(status="completed").count()

    context = {
        'pending': pending_count,
        'preparing': preparing_count,
        'shipped': shipped_count,
        'completed': completed_count,
        'order_items': order_items}
    return render(request, "retailers/order_items.html", context)


@login_required(login_url='login_wholesaler')
def update_retailer_status(request, pk):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    
    retailer = Retailer.objects.get(id=pk)
    
    
    if request.method == "POST":
    
        if retailer.is_active & retailer.user.is_active == False:
            retailer.is_active = True
            retailer.user.is_active = True
            retailer.user.save()
            retailer.save()
            AdminWholesalerLogs.objects.create(
                wholesaler = wholesaler.business_name,
                domain = domain,
                action = 'Updated Retailer Status to Active'
            )
            
        
        elif retailer.is_active & retailer.user.is_active == True:
            retailer.is_active = False
            retailer.user.is_active = False
            retailer.user.save()
            retailer.save()
            AdminWholesalerLogs.objects.create(
                wholesaler = wholesaler.business_name,
                domain = domain,
                action = 'Updated Retailer Status to Inactive'
            )


        messages.success(request, 'Account status successfully updated!') 
        return redirect('retailers')
    context = {"retailer":retailer}
    return render(request, "retailers/retailers.html", context)

 
@login_required(login_url='login_retailer')
def order_received(request, pk):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    
    retailer = wholesaler.retailers.get(id=request.user.retailer.id)
    order = Order.objects.get(id=pk)

    if request.method == "POST":
    
        order.status = "completed"
        order.save()
        retailers = Retailer.objects.get(id = request.user.retailer.id)
        RetailerLogs.objects.create(
            retailer=retailers.business_name,
            action = 'Order Recieved',             
        )

        AdminRetailerLogs.objects.create(
            wholesaler = wholesaler.business_name,
            retailer = retailer.business_name,
            domain = domain,
            action = 'Updated to order status to completed'
        )
        messages.success(request, 'Thank you!')
        return HttpResponseRedirect(reverse('dashboard_retailer') + '?status=completed')

    context = {"order":order}    
    return render(request, "retailers/dashboard.html",context)

@login_required(login_url='login_wholesaler')
def retailer_activity_logs(request):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)

    # retailers_all = RetailerLogs.objects.all()
    retailers_all, search_query = search_retailers_log(request)

    custom_range, retailers = paginate_retailers(request, retailers_all, 10)

    context ={'wholesaler':wholesaler, 'retailers':retailers, 'custom_range':custom_range, 'search_query':search_query}
    
    
    return render(request, "retailers/retailer_logs.html",context)
      