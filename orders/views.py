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
from django.http import Http404
from reportlab.pdfgen import canvas

stripe.api_key = settings.STRIPE_SECRET_KEY

# SALE REPORT IMPORTS
from django.http import JsonResponse
from django.db.models import Sum, Count
from datetime import datetime, timedelta


@login_required(login_url='login_wholesaler')
def generate_sales(request):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
     # Retrieve orders from the last 30 days
    today = datetime.now().date()
    thirty_days_ago = today - timedelta(days=30)
    orders_thirty = Order.objects.filter(created__gte=thirty_days_ago)

  # Create a new PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
    pdf_canvas = canvas.Canvas(response)

    # Add a title to the document
    pdf_canvas.setFont('Helvetica-Bold', 16)
    pdf_canvas.drawString(50, 750, 'Sales Report')

    # Define the table columns and their widths
    table_columns = ['R.O.', 'Business Name','Amount','Date']
    column_widths = [100, 100, 100, 100]

    # Add the table headers
    pdf_canvas.setFont('Helvetica-Bold', 12)
    y_offset = 700
    for index, column in enumerate(table_columns):
        pdf_canvas.drawString(50 + (index * column_widths[index]), y_offset, column)

    # Add the table data
    pdf_canvas.setFont('Helvetica', 12)
    y_offset -= 20
    total_sales = 0
    for order in orders_thirty:
        ref_num = order.reference_number
        bus_name = order.business_name
        amnt = order.total_paid 
        date = order.created

        pdf_canvas.drawString(50, y_offset, ref_num)
        pdf_canvas.drawString(50 +column_widths[0], y_offset, bus_name)
        pdf_canvas.drawString(50 + column_widths[0] + column_widths[1], y_offset, '${:.2f}'.format(amnt))
        pdf_canvas.drawString(50 +column_widths[0] + column_widths[1] + column_widths[2], y_offset, str(date))
       

        y_offset -= 20
        total_sales += amnt

        # Add a page break after every 5 rows
        if y_offset < 50:
            y_offset = 750
            pdf_canvas.showPage()
            pdf_canvas.setFont('Helvetica', 12)
            # pdf_canvas.setFont('Helvetica', 12)
            for index, column in enumerate(table_columns):
                pdf_canvas.drawString(50 + (index * column_widths[index]), y_offset, column)
            y_offset -= 20

    # Add the total sales amount
    pdf_canvas.setFont('Helvetica-Bold', 12)
    pdf_canvas.drawString(50, y_offset, 'Total')
    pdf_canvas.drawString(50 + column_widths[0], y_offset, '')
    pdf_canvas.drawString(50 + column_widths[0] + column_widths[1], y_offset, '${:.2f}'.format(total_sales))

    # Save the PDF document and return the response
    pdf_canvas.save()
    return response


@login_required(login_url='login_wholesaler')
def display_orders(request):

    if request.user.is_authenticated and (request.user.is_wholesaler or request.user.is_superuser):
        pass
    elif request.user.is_authenticated and (not request.user.is_wholesaler or not request.user.is_superuser):
        return redirect('show_shop')
    
    today = datetime.now().date()
    thirty_days_ago = today - timedelta(days=30)
    orders_thirty = Order.objects.filter(created__gte=thirty_days_ago)

    orders, search_query = search_orders(request)
    custom_range, orders = paginate_orders(request, orders, 10)
    context = {'orders': orders, 'search_query': search_query, 'custom_range':custom_range,'orders_thirty': orders_thirty}
    return render(request, 'orders/orders.html', context)


@login_required(login_url='login_retailer')
def create_order(request):
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

def create_payment_intent(amount, currency, customer, metadata):
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        customer=customer,
        metadata=metadata
    )
    return intent

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
    intent = create_payment_intent(
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
        payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
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
    if request.user.is_authenticated and (request.user.is_wholesaler or request.user.is_superuser):
        pass
    elif request.user.is_authenticated and (not request.user.is_wholesaler or not request.user.is_superuser):
        return redirect('show_shop')

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
         
    }

    # Return the data as JSON
    return JsonResponse(data)