from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.core.mail import send_mail
from .models import Order, OrderItem
from products.models import Product, Category
from django.contrib.auth.decorators import login_required
from .utils import search_orders, paginate_orders
from .forms import OrderForm
from wholesalers.models import Domain, Wholesaler
from django_tenants.utils import remove_www
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import stripe
from django.views.decorators.csrf import csrf_exempt
from retailers.models import Retailer, RetailerLogs  
from hiveadmin.models import AdminWholesalerLogs,AdminRetailerLogs

stripe.api_key = settings.STRIPE_SECRET_KEY

# SALE REPORT IMPORTS
from django.http import JsonResponse
from django.db.models import Sum, Count
from datetime import datetime, timedelta


@login_required(login_url='login_wholesaler')
def display_orders(request):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    orders, search_query = search_orders(request)
    custom_range, orders = paginate_orders(request, orders, 10)
    context = {'orders': orders, 'search_query': search_query, 'custom_range':custom_range}
    return render(request, 'orders/orders.html', context)


@login_required(login_url='login_retailer')
def create_order(request):
    try:
        request.user.retailer
    except:
        return HttpResponseForbidden()
  
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
      
    cart = request.user.cart_db_set.all()
    retailer = request.user.retailer
    
    cart_subtotal = sum(float(item.products.price) * int(item.qty) for item in cart)
    
    if cart_subtotal == 0:
        shipping = float(0.00)
    else:
        shipping = float(50.00)
    cart_total = cart_subtotal + shipping
            
    order = Order.objects.create(
        user=request.user,
        wholesaler=wholesaler,
        business_name=retailer.business_name, 
        address=retailer.address,
        total_paid=cart_total,
        success=True,
        mode_of_payment=request.POST['modeOfPayment'],
        status='pending'
    )
    
    for item in cart:
        if item.variation_id:
            OrderItem.objects.create(
                order=order, 
                product=item.products, 
                variation=item.variation_id, 
                price=item.products.price, 
                quantity=item.qty
            )
            RetailerLogs.objects.create(
                retailer=retailer.business_name,
                action = 'Retailer has placed their order', 
            )            
            AdminRetailerLogs.objects.create(
                wholesaler = wholesaler.business_name,
                retailer = retailer.business_name,
                domain = domain,
                action = 'Retailer has placed their order'
            )
        else:
            OrderItem.objects.create(
                order=order, 
                product=item.products, 
                price=item.products.price, 
                quantity=item.qty
            )
            RetailerLogs.objects.create(
                retailer=retailer.business_name,
                action = 'Retailer has placed their order',             
            )
           
            AdminRetailerLogs.objects.create(
                wholesaler = wholesaler.business_name,
                retailer = retailer.business_name,
                domain = domain,
                action = 'Retailer has placed their order'
            )       
        
    request.user.cart_db_set.filter(user=request.user).delete()
    messages.success(request, 'Your Order is successfully placed!')
    send_mail(
        'A New Order Has Been Placed',
        f'You may view and perform actions in the order at: http://{hostname_without_port}:8000/orders',
        settings.EMAIL_HOST_USER,
        [wholesaler.user.email],
        fail_silently=False
    )
    return redirect('show_shop')


@api_view(['POST'])
def stripe_intent(request):
    cart_items = request.user.cart_db_set.all()
    cart_subtotal = sum(float(item.products.price) * int(item.qty) for item in cart_items)
    
    if cart_subtotal == 0:
        shipping = float(0.00)
    else:
        shipping = float(50.00)
    cart_total = cart_subtotal + shipping
    
    metadata= {}
    for item in request.data['items']:
        metadata.update({str(item['id']): item})
 
    customer = stripe.Customer.create(email=request.data['email'])
    intent = stripe.PaymentIntent.create(
        amount=int(cart_total) * 100,
        currency='php',
        customer=customer['id'],
        metadata={str(k):str(v) for k, v in metadata.items()}
    )
    
    return Response({
        'clientSecret': intent['client_secret']
    })
   
     
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, 'whsec_e80e567c50d9affa6bc4d8518e046d7b01d7540bc3b9b7f27f584d8db425a34d'
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)


    if event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']
        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']

        send_mail(
            subject="Payment Successful",
            message="Congratulations! This is to confirm that your payment has been completed.",
            recipient_list=[customer_email],
            from_email=settings.EMAIL_HOST_USER,
        )
    return HttpResponse(status=200)


@login_required(login_url='login_wholesaler')
def order_details(request, pk):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()

    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    order_items = order.items.all()
    
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        
        if form.is_valid():
            order_form = form.save(commit=False)
            if order_form.status == 'preparing':
                for item in order_items:
                    product = Product.objects.get(id=item.product.id)
                    category = Category.objects.get(id=product.category.id)
                    category.sold += int(item.quantity)
                    product.sold += int(item.quantity)
                    if not product.variation_set.count():
                        product.actual_stocks -= int(item.quantity)           
                        product.tempo_stocks = product.actual_stocks           
                        if product.actual_stocks < 0:
                            product.actual_stocks = 0
                        elif product.tempo_stocks < 0:
                            product.tempo_stocks = 0
                        elif product.actual_stocks < 20 and product.actual_stocks >= 0:
                            send_mail(
                                f'Low Stock Level in {product.product_name}',
                                f'Low Stock Level in {product.product_name}, {product.actual_stocks} left!',
                                settings.EMAIL_HOST_USER,
                                [wholesaler.user.email],
                                fail_silently=False
                            )
                    else:
                        variation = product.variation_set.get(id=item.variation.id)
                        variation.actual_stocks_var -= int(item.quantity)
                        variation.tempo_stocks_var = variation.actual_stocks_var
                        if variation.actual_stocks_var < 0:
                            variation.actual_stocks_var = 0
                        elif variation.tempo_stocks_var < 0:
                            variation.tempo_stocks_var = 0
                        elif variation.actual_stocks_var < 20 and variation.actual_stocks_var >= 0:
                            name_var = variation.name
                            stocks_var = variation.actual_stocks_var 
                            send_mail(
                                f'Low Stock Level in {product.product_name}',
                                f'Low Stock Level in {product.product_name}, Variation: {name_var}. {stocks_var} left!',
                                settings.EMAIL_HOST_USER,
                                [wholesaler.user.email],
                                fail_silently=False
                            )
                        
                        variation.save()
                    category.save()
                    product.save()
                    
            order_form.save()
            AdminWholesalerLogs.objects.create(
                wholesaler = wholesaler.business_name,
                domain = domain,
                action = f'Updated order status to {request.POST["status"]}'
            )
            messages.success(request, 'Order status successfully updated!')
            return redirect('order_details', pk=order.id)

    
    context = {'order':order, 'order_items':order_items, 'form':form}
    return render(request, 'orders/order_details.html', context)    
    
@login_required(login_url='login_wholesaler')

def sales_report(request):
    # Retrieve orders from the last 30 days
    today = datetime.now().date()
    thirty_days_ago = today - timedelta(days=30)
    orders = Order.objects.filter(created__gte=thirty_days_ago)

    # Calculate total sales
    total_sales = orders.aggregate(total_sales=Sum('total_paid'))['total_sales']
    formatted_total_sales = "{:,}".format(total_sales)

    # Calculate average order value
    average_order_value = orders.aggregate(avg_order=Sum('total_paid')/Count('reference_number'))['avg_order']
    formatted_order_value = "{:,}".format(average_order_value)

    # # Group orders by product category and calculate revenue
    # orders_by_category = orders.values('product_category').annotate(revenue=Sum('total_paid'))

    # Create a dictionary to store the data
    data = {
        'total_sales': formatted_total_sales,
        'average_order_value': formatted_order_value,
        # 'orders_by_category': list(orders_by_category)
    }

    # Return the data as JSON
    return JsonResponse(data)