from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from wholesalers.models import Wholesaler
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Transaction, EmailTenant
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import AdminRetailerLogs, AdminWholesalerLogs


def paginate_data(request, data, results):
    page = request.GET.get('page')
    paginator = Paginator(data, results)
    
    try:
        data = paginator.page(page)  
    except PageNotAnInteger:
        page = 1 
        data = paginator.page(page)  
    except EmptyPage:
        page = paginator.num_pages 
        data = paginator.page(page)  
        
    left_index = (int(page) - 4)
    
    if left_index < 1:
        left_index = 1
        
    right_index = (int(page) + 5)
    
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
    
    custom_range = range(left_index, right_index)
    return custom_range, data

def login_user(request, redirect_page, template_name):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except BaseException:
            pass

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect(
                request.GET['next'] if 'next' in request.GET else redirect_page)
        else:
            messages.error(request, 'Invalid Username or Password!')
            return redirect(
                request.GET['next'] if 'next' in request.GET else redirect_page)

    
    return render(request, template_name)


def logout_user(request, redirect_page):
    logout(request)
    return redirect(redirect_page)

#Search bar and flter to search wholesalers
def search_wholesaler(request):
    search_query = ''
    filter_query = ''
   
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    if request.GET.get('category'):
        filter_query = request.GET.get('category')

    status_filter = None

    if filter_query == 'True':
        status_filter = True
    elif filter_query == 'False':
        status_filter = False

    if search_query:
        wholesalers = Wholesaler.objects.filter(Q(is_active__exact=status_filter) | Q(business_name__icontains=search_query)).exclude(id=1)
    elif status_filter is not None:
        wholesalers = Wholesaler.objects.filter(Q(is_active__exact=status_filter)).exclude(id=1)
    else:
        wholesalers = Wholesaler.objects.exclude(id=1)
        
    return wholesalers, search_query

#Search bar and flter to search admins
def search_admins(request):
    search_query = ''
    retailer_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    if request.GET.get('category'):
        retailer_query = request.GET.get('category')
    
    status_filter = User.objects.filter(is_active__icontains=retailer_query)

    admin = User.objects.distinct().filter((Q(is_superuser=False) & Q(is_staff=True))
                                           & Q(id__in=status_filter) & 
                                                    (Q(first_name__icontains=search_query) |
                                                    Q(last_name__icontains=search_query))).exclude(pk=1)

    return admin, search_query

#search bar and filter for transactions 
def search_transaction(request):
    search_query = ''
    transaction_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    if request.GET.get('category'):
        transaction_query = request.GET.get('category')
    
    status_filter = Transaction.objects.filter(payment_status__icontains=transaction_query)

    transactions = Transaction.objects.distinct().filter(Q(id__in=status_filter) & 
                                                    (Q(business_name__icontains=search_query) |
                                                    Q(payment_method__icontains=search_query)
                                                    | Q(payment_status__icontains=search_query)))

    return transactions, search_query


#search bar and filter for transactions 
def search_logs(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    email_tenant = EmailTenant.objects.distinct().filter(Q(email__icontains=search_query) |
                                                    Q(status__icontains=search_query))

    return email_tenant, search_query


def search_wholesaler_logs(request):
    search_query = ''
   
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    

    wholesalers_activity = AdminWholesalerLogs.objects.distinct().filter(Q(wholesaler__icontains=search_query) | Q(domain__icontains=search_query))
        
    return wholesalers_activity, search_query

def search_retailer_logs(request):
    search_query = ''
   
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    

    retailers_activity = AdminRetailerLogs.objects.distinct().filter(Q(wholesaler__icontains=search_query) | Q(retailer__icontains=search_query) | Q(domain__icontains=search_query))
        
    return retailers_activity, search_query
