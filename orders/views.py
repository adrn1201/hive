from django.shortcuts import render

def display_orders(request):
    return render(request, 'orders/orders.html')
