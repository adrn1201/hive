from django.shortcuts import render, get_object_or_404
from products.models import Inventory
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from products.models import Inventory
from .cart import Cart
from .models import Cart_DB


@login_required(login_url='login_retailer')
def show_cart(request):
    return render(request, "cart/shop_cart.html")


@api_view(['POST'])
def cart_delete(request):
    cart= Cart(request)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.data['productid']
        cart.delete(product=product_id)
        
        item = request.user.cart_db_set.get(product_id=product_id)
        item.delete()
        
        cart_qty = cart.__len__()
        cart_subtotal = cart.get_subtotal_price()
        cart_total = cart.get_total_price()
 
        response = Response({
            'qty': cart_qty, 
            'subtotal':cart_subtotal,
            'total': cart_total
        })
        return response
    return Response({'none':'none'})
    
    
@api_view(['POST'])
def cart_add(request):
    cart = Cart(request)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.data['productid']
        product_qty = request.data['productqty']
        product = get_object_or_404(Inventory, id=product_id)
        cart.add(product=product, qty=product_qty)
        cart_db = Cart_DB(
            user=request.user,
            product_id=product.id,
            qty=product_qty
        )
        cart_db.save()
        
        cart_qty = cart.__len__()
        response = Response({'qty': cart_qty})
        return response
    
    return Response({'none':'none'})


@api_view(['POST'])
def cart_update(request):
    cart = Cart(request)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.data['productid']
        product_qty = request.data['productqty']
        cart.update(product=product_id, qty=product_qty)
        item = request.user.cart_db_set.get(product_id=product_id)
        item.qty = product_qty
        item.save()
        
        cart_qty = cart.__len__()
        cart_subtotal = cart.get_subtotal_price()
        cart_total = cart.get_total_price()
 
        response = Response({
            'qty': cart_qty, 
            'subtotal':cart_subtotal,
            'total': cart_total
        })
        return response
    return Response({'none':'none'})


