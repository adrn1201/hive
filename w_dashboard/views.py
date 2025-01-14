from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django_tenants.utils import remove_www
from wholesalers.models import Domain, Wholesaler
from django.db.models import Sum
from django.db.models import Q
from django.db.models.functions import ExtractWeek, ExtractYear, ExtractMonth
import datetime

@login_required(login_url='login_wholesaler')
def w_dashboard(request):    
    if request.user.is_authenticated and (request.user.is_wholesaler or request.user.is_superuser):
        pass
    elif request.user.is_authenticated and (not request.user.is_wholesaler or not request.user.is_superuser):
        return redirect('show_shop')
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    
    pending = wholesaler.order_set.filter(status='pending').count()
    preparing = wholesaler.order_set.filter(status='preparing').count()
    shipped = wholesaler.order_set.filter(status='shipped').count()
    completed = wholesaler.order_set.filter(status='completed').count()
    
    weekly_stats = (wholesaler.order_set.distinct().filter(Q(mode_of_payment='Credit Card/Debit Card') | Q(status='completed')|Q(status='shipped'))
    .annotate(year=ExtractYear('created'))
    .annotate(week=ExtractWeek('created'))
    .values('year', 'week')
    .annotate(total=Sum('total_paid'))
    ).order_by("-year", "-week")
    
    monthly_stats = (wholesaler.order_set.distinct().filter(Q(mode_of_payment='Credit Card/Debit Card') | Q(status='completed')|Q(status='shipped'))
    .annotate(year=ExtractYear('created'))
    .annotate(month=ExtractMonth('created'))
    .values('year', 'month')
    .annotate(total=Sum('total_paid'))
    ).order_by("-year", "-month")
    
    daily_sales = wholesaler.order_set.distinct().filter(
        Q(mode_of_payment='Credit Card/Debit Card') |
        Q(status='completed')|Q(status='shipped')).values("created").order_by("-created").annotate(sum=Sum('total_paid'))[:7] 
    
    weekly_sales = []
    monthly_sales = []

    for record in weekly_stats:
        week = "{year}-W{week}-1".format(year=record['year'], week=record['week'])
        timestamp = datetime.datetime.strptime(week, "%Y-W%W-%w")
        sales = record['total']
        weekly_sales.append({'created':timestamp, 'sum':sales})

    for record in monthly_stats:
        timestamp = datetime.datetime(year=record['year'], month=record['month'], day=1).date()
        sales = record['total']
        monthly_sales.append({'created':timestamp, 'sum':sales})


    products = wholesaler.product_set.all().order_by("-sold")
    
    recent_orders = wholesaler.order_set.all().order_by('-created')
    
    context = {
        'daily_sales':daily_sales,
        'weekly_sales':weekly_sales[:7],
        'monthly_sales':monthly_sales[:7],
        'products':products, 
        'pending' :pending,
        'preparing': preparing,
        'shipped':shipped,
        'completed':completed,
        'recent_orders':recent_orders,
    }
    
    return render(request, 'w_dashboard/dashboard.html', context)
