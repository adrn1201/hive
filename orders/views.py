from django.shortcuts import render, redirect
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


@login_required(login_url='login_wholesaler')
def display_orders(request):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    orders, search_query = search_orders(request)
    custom_range, orders = paginate_orders(request, orders, 15)
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
        else:
            OrderItem.objects.create(
                order=order, 
                product=item.products, 
                price=item.products.price, 
                quantity=item.qty
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
            messages.success(request, 'Order status successfully updated!')
            return redirect('order_details', pk=order.id)

    
    context = {'order':order, 'order_items':order_items, 'form':form}
    return render(request, 'orders/order_details.html', context)    
    
