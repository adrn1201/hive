from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from hiveadmin.models import Transaction
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django_tenants.utils import remove_www
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Domain, Wholesaler




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


#search bar and filter for transactions 
def search_transaction(request):
    search_query = ''

    if request.GET.get('q'):
        search_query = request.GET.get('q')

    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)   
        
    # transactions = Transaction.objects.distinct().filter(Q(business_name__icontains=search_query) |
    #                                                 Q(payment_status__icontains=search_query))
    
    transactions = wholesaler.order_set.filter(Q(mode_of_payment="Credit Card/Debit Card") &
                                                    (Q(success__icontains=search_query)
                                                    | Q(business_name__icontains=search_query)))

    return transactions, search_query