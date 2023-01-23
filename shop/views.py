from django.shortcuts import render

def show_shop(request):
    return render(request, "shop/shop.html")
