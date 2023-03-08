from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, WholesalerCreationForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .models import Domain, Wholesaler
from django_tenants.utils import remove_www
from django_tenants.utils import schema_context
from orders.models import Order, OrderItem
from hiveadmin.models import Transaction
from hiveadmin.models import AdminWholesalerLogs,AdminRetailerLogs
from .utils import search_transaction, paginate_data

user_credentials = ''

def register_wholesalers(request):
    if request.GET.get('session_id'):
        pass
    else:
        return redirect('checkout')
    
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.is_wholesaler = True
            global user_credentials
            user_credentials = user
            return redirect('wholesaler_create_profile', checkout=request.GET.get('session_id'))

        else:
            pass
    context = {'form': form}
    return render(request, "wholesalers/create_wholesalers.html", context)


def wholesaler_create_profile(request, checkout):
    form = WholesalerCreationForm()
    if request.method == "POST":
        form = WholesalerCreationForm(request.POST, request.FILES)
        if form.is_valid():
            wholesaler = form.save(commit=False)
            wholesaler.schema_name = wholesaler.business_name.lower()
            context_schema = wholesaler.schema_name
            wholesaler.is_active = True
            user_credentials.save()
            wholesaler.user = user_credentials
            wholesaler.save()

            domain = Domain()
            domain.domain = str(
                wholesaler.business_name.replace(
                    ' ', '-').lower()) + '.localhost'
            redirect_url = domain.domain
            domain.tenant = wholesaler
            domain.is_primary = True
            domain.save()

            with schema_context(context_schema):
                user_credentials.save()

            return redirect(f'http://{redirect_url}:8000/account/wholesalers/login/')

    context = {'form': form}
    return render(request, 'wholesalers/wholesaler_profile.html', context)


@login_required(login_url='login_wholesaler')
def wholesaler_view_profile(request):
    if request.user.is_authenticated and (request.user.is_wholesaler or request.user.is_superuser):
        pass
    elif request.user.is_authenticated and (not request.user.is_wholesaler or not request.user.is_superuser):
        return redirect('show_shop')
    
    wholesaler = request.user.wholesaler
    context ={'wholesaler' : wholesaler}
    return render(request, "wholesalers/wholesaler_view_profile.html", context)


@login_required(login_url='login_wholesaler')
def wholesaler_edit_profile(request):
    if request.user.is_authenticated and (request.user.is_wholesaler or request.user.is_superuser):
        pass
    elif request.user.is_authenticated and (not request.user.is_wholesaler or not request.user.is_superuser):
        return redirect('show_shop')
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    form = WholesalerCreationForm(instance=wholesaler)
    if request.method == "POST":
        form = WholesalerCreationForm(request.POST, request.FILES, instance=wholesaler)
        if form.is_valid():
            wholesaler = form.save(commit=False)
            wholesaler.color = request.POST['color']
            wholesaler.save()
            AdminWholesalerLogs.objects.create(
                wholesaler = wholesaler.business_name,
                domain = domain,
                action = 'Updated Profile'
            )
            return redirect('wholesaler_view_profile')


    context = {'form':form, 'wholesaler':wholesaler}
    return render(request, 'wholesalers/wholesaler_edit_profile.html', context)
   

@login_required(login_url='login_wholesaler')
def email_retailer(request):
    if request.user.is_authenticated and (request.user.is_wholesaler or request.user.is_superuser):
        pass
    elif request.user.is_authenticated and (not request.user.is_wholesaler or not request.user.is_superuser):
        return redirect('show_shop')
    
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


@login_required(login_url='login_wholesaler')
def transactions(request):
    if request.user.is_authenticated and (request.user.is_wholesaler or request.user.is_superuser):
        pass
    elif request.user.is_authenticated and (not request.user.is_wholesaler or not request.user.is_superuser):
        return redirect('show_shop')
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)   
    
    transactions, search_query = search_transaction(request)
    custom_range, transactions = paginate_data(request, transactions, 10)

    # transactions = wholesaler.order_set.filter(Q(mode_of_payment="Credit Card/Debit Card") & Q(success=True))
    context = {'transactions':transactions, 'search_query':search_query, 'custom_range':custom_range}
    return render (request, 'wholesalers/transactions.html', context)


@login_required(login_url='login_wholesaler')
def transaction_details(request, pk):
    if request.user.is_authenticated and (request.user.is_wholesaler or request.user.is_superuser):
        pass
    elif request.user.is_authenticated and (not request.user.is_wholesaler or not request.user.is_superuser):
        return redirect('show_shop')
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    
    order = Order.objects.get(id=pk)
    order_items = order.items.all()
    
    context = {'order':order, 'order_items':order_items}
    return render(request, 'wholesalers/details.html', context)