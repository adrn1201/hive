from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from cart.cart import Cart
from .models import Order, OrderItem
from products.models import Inventory, Category
from django.contrib.auth.decorators import login_required
from .utils import search_orders, paginate_orders

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
    
    cart = Cart(request)
    retailer = request.user.retailer
    wholesaler = request.user.retailer.wholesaler
    cart_total = cart.get_total_price()
            
    order = Order.objects.create(
        user=request.user,
        wholesaler=wholesaler,
        business_name=retailer.business_name, 
        total_paid=cart_total,
        mode_of_payment=request.POST['modeOfPayment'],
        status='pending'
    )
    
    for item in cart:
        order_item = OrderItem.objects.create(
            order=order, 
            product=item['product'], 
            price=item['price'], 
            quantity=item['qty']
        )
        inventory = Inventory.objects.get(id=order_item.product.id)
        category = Category.objects.get(id=inventory.category.id)
        category.sold += int(order_item.quantity)
        inventory.sold += int(order_item.quantity)
        inventory.actual_quantity -= int(order_item.quantity)
        category.save()
        inventory.save()
    
    cart.clear()
    request.user.cart_db_set.filter(user=request.user).delete()
    messages.success(request, 'Your Order is successfully placed!')
    return redirect('show_shop')
