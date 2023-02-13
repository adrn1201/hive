from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import Order, OrderItem

def display_orders(request):
    wholesaler = request.user.wholesaler
    orders = wholesaler.order_set.all()
    context = {'orders':orders}
    return render(request, 'orders/orders.html', context)


def create_order(request):
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
    return redirect('show_shop')
