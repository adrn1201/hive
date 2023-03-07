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

user_credentials = ''

def register_wholesalers(request):
    try:
        if request.user.is_authenticated and request.user.wholesaler:
            return redirect('w_dashboard')
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
            return redirect('wholesaler_create_profile')

        else:
            pass
    context = {'form': form}
    return render(request, "wholesalers/create_wholesalers.html", context)


def wholesaler_create_profile(request):
    try:
        if request.user.is_authenticated and request.user.wholesaler:
            return redirect('w_dashboard')
    except:
        return HttpResponseForbidden()

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
    try:
        request.user.wholesaler
    except BaseException:
        return HttpResponseForbidden()
    wholesaler = request.user.wholesaler
    context ={'wholesaler' : wholesaler}
    return render(request, "wholesalers/wholesaler_view_profile.html", context)


@login_required(login_url='login_wholesaler')
def wholesaler_edit_profile(request):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
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
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
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
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)   
    
    transactions = wholesaler.order_set.filter(Q(mode_of_payment="Credit Card/Debit Card") & Q(success=True))
    context = {'transactions':transactions}
    return render (request, 'wholesalers/transactions.html', context)


@login_required(login_url='login_wholesaler')
def transaction_details(request, pk):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()

    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)

    order = Order.objects.get(id=pk)
    order_items = order.items.all()
    
    context = {'order':order, 'order_items':order_items}
    return render(request, 'wholesalers/details.html', context)