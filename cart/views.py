from django.shortcuts import render, get_object_or_404
from products.models import Inventory
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import Inventory
from .cart import Cart

def show_cart(request):
    return render(request, "cart/shop_cart.html")

@api_view(['POST'])
def cart_delete(request):
    cart= Cart(request)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.data['productid']
        cart.delete(product=product_id)
        cart_qty = cart.__len__()
        cart_total = cart.get_total_price()
        response = Response({
            'qty': cart_qty, 
            'subtotal':cart_total
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
        
        cart_qty = cart.__len__()
        response = Response({'qty': cart_qty})
        return response
    
    return Response({'none':'none'})



