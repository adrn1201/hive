from django.shortcuts import render, redirect, get_object_or_404
from django_tenants.utils import remove_www
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from wholesalers.models import Wholesaler
from wholesalers.models import Domain
from .models import Retailer
from orders.models import Order, OrderItem
from .forms import RetailerCreationForm, CustomUserCreationForm

user_credentials = ''


def register_retailer(request):
    try:
        if request.user.is_authenticated and request.user.retailer:
            return redirect('show_shop')
    except BaseException:
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
    context = {'form': form}
    return render(request, "retailers/create_retailer.html", context)


def retailer_create_profile(request):
    try:
        if request.user.is_authenticated and request.user.retailer:
            return redirect('show_shop')
    except BaseException:
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

    context = {'form': form}
    return render(request, 'retailers/retailers_profile.html', context)


@login_required(login_url='login_wholesaler')
def retailer_edit_profile(request):
    try:
        request.user.retailer
    except BaseException:
        return HttpResponseForbidden()
    retailer = request.user.retailer
    form = RetailerCreationForm(instance=retailer)
    if request.method == "POST":
        form = RetailerCreationForm(request.POST, instance=retailer)
        if form.is_valid():
            form.save()
            return redirect('retailer_edit_profile')

    context = {'form': form}
    return render(request, 'retailers/retailer_edit_profile.html', context)


@login_required(login_url='login_wholesaler')
def index(request):
    try:
        request.user.wholesaler
    except BaseException:
        return HttpResponseForbidden()

    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    retailers = Retailer.objects.filter(wholesaler=wholesaler_id)
    context = {'retailers':retailers}
    return render(request, "retailers/retailers.html", context)


@login_required(login_url='login_retailer')
def dashboard_retailer(request):
    order_status = ''
    orders = ''
    if request.GET.get('status'):
        order_status = request.GET.get('status')
        orders = request.user.order_set.distinct().filter(status=order_status)
    else:
        orders = request.user.order_set.all()
    pending_count = request.user.order_set.distinct().filter(status="pending").count()
    preparing_count = request.user.order_set.distinct().filter(status="preparing").count()
    shipped_count = request.user.order_set.distinct().filter(status="shipped").count()
    completed_count = request.user.order_set.distinct().filter(status="completed").count()
    context = {
        'orders': orders,
        'pending': pending_count,
        'preparing': preparing_count,
        'shipped': shipped_count,
        'completed': completed_count}
    return render(request, "retailers/dashboard.html", context)


@login_required(login_url='login_retailer')
def order_items(request, pk):
    order = Order.objects.get(id=pk)
    order_items = order.items.all()
    context = {'order_items': order_items}
    return render(request, "retailers/order_items.html", context)
