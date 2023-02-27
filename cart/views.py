from django.shortcuts import render, get_object_or_404
from products.models import Product
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from products.models import Product
from .models import Cart_DB
from django.conf import settings


@login_required(login_url='login_retailer')
def show_cart(request):
    cart_items = request.user.cart_db_set.all()
    cart_subtotal = sum(float(item.products.price) * int(item.qty) for item in cart_items)
    
    if cart_subtotal == 0:
        shipping = float(0.00)
    else:
        shipping = float(50.00)
    cart_total = cart_subtotal + shipping
    context = {'cart_items':cart_items, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY ,'cart_total':cart_total, 'cart_subtotal':cart_subtotal}
    return render(request, "cart/shop_cart.html", context)


@api_view(['POST'])
def cart_delete(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.data['productid']
        product_qty = request.data['productqty']
        item = request.user.cart_db_set.get(id=int(request.data['cartId']))
        item.delete()
        product = get_object_or_404(Product, id=product_id)
        
        if item.variation_id:
            variation = product.variation_set.get(id=item.variation_id.id)
            variation.tempo_stocks_var += int(product_qty)
            variation.save()
        else:
            product.tempo_stocks += int(product_qty)
            product.save()
                
        cart_items = request.user.cart_db_set.all()
        cart_subtotal = sum(float(item.products.price) * int(item.qty) for item in cart_items)
        
        if cart_subtotal == 0:
            shipping = float(0.00)
        else:
            shipping = float(50.00)
        cart_total = cart_subtotal + shipping
 
        response = Response({
            'qty': request.user.cart_db_set.all().count(), 
            'subtotal':cart_subtotal,
            'total': cart_total
        })
        return response
    return Response({'none':'none'})
    
    
@api_view(['POST'])
def cart_add(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.data['productid']
        product_qty = request.data['productqty']
        variation_id = ''
        variation = ''
        product = get_object_or_404(Product, id=product_id)
        if request.data['variation']:
            variation_id = request.data['variation']
            variation = product.variation_set.get(id=variation_id)
        
        data_created = False
        products_data = request.user.cart_db_set.filter(products=product)
        if variation and not products_data:
            Cart_DB.objects.create(
                user=request.user,
                products=product,
                variation_id=variation,
                qty=product_qty,
                subtotal=product.price * int(product_qty)
            )
            variation.tempo_stocks_var -= int(product_qty)
            if variation.tempo_stocks_var < 0:
                variation.tempo_stocks_var = 0
            variation.save()
        elif variation and products_data:
            for item in products_data:
                if variation.id == item.variation_id.id:
                    item.qty += int(product_qty)
                    item.subtotal+=product.price * int(product_qty)
                    item.save()
                    variation.tempo_stocks_var -= int(product_qty)
                    if variation.tempo_stocks_var < 0:
                        variation.tempo_stocks_var = 0
                    variation.save()
                    data_created = True
                    
        elif not variation and not products_data:
            Cart_DB.objects.create(
                user=request.user,
                products=product,
                qty=product_qty,
                subtotal=product.price * int(product_qty)
            )
            product.tempo_stocks -= int(product_qty)
            if product.tempo_stocks < 0:
                product.tempo_stocks = 0
            product.save()
        elif not variation and products_data:
            for item in products_data:
                cart_item = product.products_cart.get(products=product)
                cart_item.qty += int(product_qty)
                cart_item.subtotal+=product.price * int(product_qty)
                cart_item.save()
                product.tempo_stocks -= int(product_qty)
                if product.tempo_stocks < 0:
                    product.tempo_stocks = 0
                product.save()

        if variation and products_data and not data_created:
            Cart_DB.objects.create(
                user=request.user,
                products=product,
                variation_id=variation,
                qty=product_qty,
                subtotal=product.price * int(product_qty)
            )
            variation.tempo_stocks_var -= int(product_qty)
            if variation.tempo_stocks_var < 0:
                variation.tempo_stocks_var = 0
                variation.save()
        
        cart_qty = request.user.cart_db_set.all().count()
        if variation:
            new_quantity = variation.tempo_stocks_var
            var_id = variation.id
        else:
            new_quantity = product.tempo_stocks
            var_id = ''
        response = Response({'qty': cart_qty, 'new_quantity': new_quantity, 'var_id': var_id})
        return response
    
    return Response({'none':'none'})


@api_view(['POST'])
def cart_update(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.data['productid']
        product_qty = request.data['productqty']
        cart_id = request.data['cartId']
        product = get_object_or_404(Product, id=product_id)
        
        item = request.user.cart_db_set.get(id=int(cart_id))
        item.qty = product_qty
        item.subtotal=product.price * int(product_qty)
        item.save()
        
        variation = ''
        if item.variation_id:
            variation = product.variation_set.get(id=item.variation_id.id)
            
            if request.data['status'] == 'increase-btn':
                variation.tempo_stocks_var -= 1
            elif request.data['status'] == 'decrease-btn':
                variation.tempo_stocks_var += 1
            elif request.data['status'] == 'increase':
                variation.tempo_stocks_var -=  int(product_qty)
            elif request.data['status'] == 'decrease':
                variation.tempo_stocks_var +=  int(product_qty)
                
            if variation.tempo_stocks_var < 0:
                variation.tempo_stocks_var = 0
            variation.save()
        else:
            if request.data['status'] == 'increase-btn':
                product.tempo_stocks -= 1
            elif request.data['status'] == 'decrease-btn':
                product.tempo_stocks += 1
            elif request.data['status'] == 'increase':
                product.tempo_stocks -=  int(product_qty)
            elif request.data['status'] == 'decrease':
                product.tempo_stocks +=  int(product_qty)
            
            if product.tempo_stocks < 0:
                product.tempo_stocks = 0
            product.save()
        
        cart_items = request.user.cart_db_set.all()
        cart_subtotal = sum(float(item.products.price) * int(item.qty) for item in cart_items)
        
        if cart_subtotal == 0:
            shipping = float(0.00)
        else:
            shipping = float(50.00)
        cart_total = cart_subtotal + shipping
 
        if variation:
            new_quantity = variation.tempo_stocks_var
            print(new_quantity)
            var_id = variation.id
        else:
            new_quantity = product.tempo_stocks
            var_id = ''
            
        response = Response({
            'qty': request.user.cart_db_set.all().count(),
            'subtotal':cart_subtotal,
            'total': cart_total, 
            'new_quantity': new_quantity, 
            'var_id': var_id
        })
        return response
    return Response({'none':'none'})


