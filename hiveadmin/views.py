from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponse
from wholesalers.models import Wholesaler
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .utils import login_user, logout_user, search_wholesaler, search_admins, search_transaction, paginate_data, search_logs, search_wholesaler_logs, search_retailer_logs
import stripe
from django.views.decorators.csrf import csrf_exempt
from .models import Transaction, EmailTenant
from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import ExtractYear, ExtractMonth
import datetime
from .models import AdminRetailerLogs, AdminWholesalerLogs


@login_required(login_url='login_admin')
def wholesaler_activity_logs(request):
    if request.user.is_authenticated and request.user.is_superuser:
        pass
    elif request.user.is_authenticated and not request.user.is_superuser:
        return redirect('login_admin')
    

    wholesalers, search_query = search_wholesaler_logs(request)
    custom_range, wholesaler_logs = paginate_data(request, wholesalers, 1)
    context = {'wholesaler_logs':wholesaler_logs, 'search_query':search_query,'custom_range':custom_range}
    return render(request, 'hiveadmin/wholesaler_logs.html', context)

@login_required(login_url='login_admin')
def retailer_activity_logs(request):
    if request.user.is_authenticated and request.user.is_superuser:
        pass
    elif request.user.is_authenticated and not request.user.is_superuser:
        return redirect('login_admin')
    
    retailers, search_query = search_retailer_logs(request)
    custom_range, retailer_logs = paginate_data(request, retailers, 1)
    context = {'retailer_logs':retailer_logs, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'hiveadmin/retailer_logs.html',context)



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
            user.is_superuser = False
            user.is_staff = True
            user.save()
            global user_credentials
            user_credentials = user
            return redirect('admins')
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
    if request.user.is_authenticated and request.user.is_superuser or request.user.is_staff:
        pass
    elif request.user.is_authenticated and not request.user.is_superuser or not request.user.is_staff:
        return redirect('login_admin')
    
    transactions = Transaction.objects.all()
    wholesalers = Wholesaler.objects.all().exclude(id=1)

    monthly_stats = (Transaction.objects.distinct().all()
    .annotate(year=ExtractYear('created'))
    .annotate(month=ExtractMonth('created'))
    .values('year', 'month')
    .annotate(total=Sum('amount'))
    )

    monthly_sales = []

    for record in monthly_stats:
        timestamp = datetime.datetime(year=record['year'], month=record['month'], day=1).date()
        sales = record['total']
        monthly_sales.append({'created':timestamp, 'sum':sales})
    
    context ={'transactions': transactions, 'wholesalers': wholesalers, 'monthly_sales' : monthly_sales}
    return render(request, 'hiveadmin/dashboard.html', context)

@login_required(login_url='login_admin')
def list_wholesalers(request): 

    if request.user.is_authenticated and request.user.is_superuser or request.user.is_staff:
        pass
    elif request.user.is_authenticated and not request.user.is_superuser or not request.user.is_staff:
        return redirect('login_admin')
    
    wholesalers, search_query = search_wholesaler(request)
    custom_range, wholesalers = paginate_data(request, wholesalers, 10)
    context = {'wholesalers': wholesalers, 'search_query': search_query, 'custom_range': custom_range }

    if(request.method == "POST"):
        send_mail(
            'Hive Account Registration',
            'Please click the link to register your account http://localhost:8000/hiveadmin/checkout/',
            settings.EMAIL_HOST_USER,
            [request.POST['email']],
            fail_silently=False
        )
        EmailTenant.objects.create(
            email=request.POST['email'],
            status = True,             
        )
        messages.success(request, 'Registration has been successfully sent!')
        return redirect('list_wholesalers')
    return render(request, 'hiveadmin/wholesalers_list.html',context)

@login_required(login_url='login_admin')
def transactions(request):
    if request.user.is_authenticated and request.user.is_superuser or request.user.is_staff:
        pass
    elif request.user.is_authenticated and not request.user.is_superuser or not request.user.is_staff:
        return redirect('login_admin')
    
    transactions, search_query = search_transaction(request)
    custom_range, transactions = paginate_data(request, transactions, 10)

    # transaction = Transaction.objects.all()
    context ={'transactions':transactions ,'searches':search_query, 'custom_range':custom_range}
    
    return render(request, 'hiveadmin/transactions.html', context)

@login_required(login_url='login_admin')
def admins(request):
    if request.user.is_authenticated and request.user.is_superuser:
        pass
    elif request.user.is_authenticated and not request.user.is_superuser:
        return redirect('login_admin')
    
    admin, search_query = search_admins(request)
    custom_range, admin = paginate_data(request, admin, 10)

    context = {'admin': admin, 'search_query': search_query, 'custom_range': custom_range}

    return render(request, 'hiveadmin/list_admin.html', context)

def update_admin_status(request, pk):
    user = User.objects.get(pk=pk)

    if request.method == 'POST':
        user.is_active = request.POST['status']
        user.save()
    return redirect('admins')
    

@login_required(login_url='login_admin')
def registration_logs (request):
    if request.user.is_authenticated and request.user.is_superuser or request.user.is_staff:
        pass
    elif request.user.is_authenticated and not request.user.is_superuser or not request.user.is_staff:
        return redirect('login_admin')
    
    email_tenant, search_query = search_logs(request)
    custom_range, email_tenant = paginate_data(request, email_tenant, 10)

    # emailTenat = EmailTenant.objects.all()
    context ={'email_tenant':email_tenant, 'search_query':search_query, 'custom_range':custom_range}

    return render(request, 'hiveadmin/logs.html', context)

@login_required(login_url='login_admin')
def update_wholesaler(request, pk):

    if request.user.is_authenticated and request.user.is_superuser or request.user.is_staff:
        pass
    elif request.user.is_authenticated and not request.user.is_superuser or not request.user.is_staff:
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
        
def checkout (request):
    
    return render(request, 'hiveadmin/checkout.html')


stripe.api_key = settings.STRIPE_SECRET_KEY_ADMIN

def checkout_session_payment (request):

    if request.method == 'POST':
        prices = stripe.Price.list(
            lookup_keys=[request.POST['lookup_key']],
            expand=['data.product']
        )

    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price': prices.data[0].id,
                'quantity': 1,
            },
        ],
        custom_fields=[
            {
            "key": "business",
            "label": {"type": "custom", "custom": "Business Name"},
            "type": "text",
            },
        ],
        mode='subscription',
        success_url='http://localhost:8000/wholesalers/register',
        cancel_url='http://localhost:8000/hiveadmin/checkout',
    )
    return redirect(checkout_session.url, code=303)

def success_payment (request):

    return render(request, 'hiveadmin/success.html')
      
    
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET_ADMIN


def customer_portal(request):
    # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
    # Typically this is stored alongside the authenticated user in your database.
    session_id = request.GET.get('session_id')
    checkout_session = stripe.checkout.Session.retrieve(session_id)

    portal_session = stripe.billing_portal.Session.create(
        customer=checkout_session.customer,
        return_url=request.build_absolute_uri('/hiveadmin/'),
    )

    return redirect(portal_session.url)


@csrf_exempt
def webhook_received(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, 'whsec_ed777af4856f089afc4bc020814eaa4d3f6d5dc39b2426aed3e29ad429a8bf6e'

        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        subscription = event['data']['object']
        Transaction.objects.create(
            business_name=subscription['custom_fields'][0]['text']['value'],
            payment_method = 'Credit Card/Debit Card',             
            payment_status = 'Success',
            amount = subscription['amount_total'] / 100,
            subscription_id = subscription['subscription']
        )

        stripe_customer_id = subscription["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']

        send_mail(
            subject="Payment Successful",
            message="Congratulations! This is to confirm that your payment has been completed." +
              "CUSTOMER PORTAL: https://billing.stripe.com/p/login/test_fZe9C06S760t5qg288",
            recipient_list=[customer_email],
            from_email=settings.EMAIL_HOST_USER,
        )
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        if subscription['cancel_at_period_end']:
            transaction = Transaction.objects.filter(subscription_id=subscription['id'])[0]
            transaction.payment_status = 'Cancelled'
            transaction.save()


    return HttpResponse(status=200)
