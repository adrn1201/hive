from django.shortcuts import render
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
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    
    pending = wholesaler.order_set.filter(status='pending').count()
    preparing = wholesaler.order_set.filter(status='preparing').count()
    shipped = wholesaler.order_set.filter(status='shipped').count()
    completed = wholesaler.order_set.filter(status='completed').count()
    
    weekly_stats = (wholesaler.order_set.distinct().filter(Q(mode_of_payment='Credit Card/Debit Card') | Q(mode_of_payment='Cash on Delivery') | Q(status='completed'))
    .annotate(year=ExtractYear('created'))
    .annotate(week=ExtractWeek('created'))
    .values('year', 'week')
    .annotate(total=Sum('total_paid'))
    )
    
    monthly_stats = (wholesaler.order_set.distinct().filter(Q(mode_of_payment='Credit Card/Debit Card') | Q(mode_of_payment='Cash on Delivery') | Q(status='completed'))
    .annotate(year=ExtractYear('created'))
    .annotate(month=ExtractMonth('created'))
    .values('year', 'month')
    .annotate(total=Sum('total_paid'))
    )
    
    daily_sales = wholesaler.order_set.distinct().filter(
        Q(mode_of_payment='Credit Card/Debit Card') |
        Q(mode_of_payment='Cash on Delivery') |
        Q(status='completed')).values("created").order_by("created").annotate(sum=Sum('total_paid'))
    
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
        'weekly_sales':weekly_sales,
        'monthly_sales':monthly_sales,
        'products':products, 
        'pending' :pending,
        'preparing': preparing,
        'shipped':shipped,
        'completed':completed,
        'recent_orders':recent_orders,
    }
    
    return render(request, 'w_dashboard/dashboard.html', context)
