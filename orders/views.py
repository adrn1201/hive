from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from cart.cart import Cart
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required


@login_required(login_url='login_wholesaler')
def display_orders(request):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
    wholesaler = request.user.wholesaler
    orders = wholesaler.order_set.all()
    context = {'orders':orders}
    return render(request, 'orders/orders.html', context)


@login_required(login_url='login_retailer')
def create_order(request):
    try:
        request.user.retailer
    except:
        return HttpResponseForbidden()
    
    cart = Cart(request)
    order_status = ''
    retailer = request.user.retailer
    wholesaler = request.user.retailer.wholesaler
    cart_total = cart.get_total_price()
    
    if request.POST['modeOfPayment'] == 'Cash on Delivery':
        order_status = 'pending'
        
    order = Order.objects.create(
        user=request.user,
        wholesaler=wholesaler,
        business_name=retailer.business_name, 
        total_paid=cart_total,
        mode_of_payment=request.POST['modeOfPayment'],
        status=order_status
    )
    
    for item in cart:
        OrderItem.objects.create(
            order=order, 
            product=item['product'], 
            price=item['price'], 
            quantity=item['qty']
        )
    
    cart.clear()
    request.user.cart_db_set.filter(user=request.user).delete()
    messages.success(request, 'Your Order is successfully placed!')
    return redirect('show_shop')
