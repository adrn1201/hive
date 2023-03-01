from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from wholesalers.models import Wholesaler
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout


def login_user(request, redirect_page, template_name):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except BaseException:
            pass

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect(
                request.GET['next'] if 'next' in request.GET else redirect_page)
        else:
            messages.error(request, 'Invalid Username or Password!')
            return redirect(
                request.GET['next'] if 'next' in request.GET else redirect_page)

    
    return render(request, template_name)


def logout_user(request, redirect_page):
    logout(request)
    return redirect(redirect_page)

def search_products(request):
    search_query = ''
    status_query = ''
   
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    if request.GET.get('status'):
        status_query = request.GET.get('status')
    
    status_search = Wholesaler.objects.filter(name__icontains=search_query)
    status_filter = Wholesaler.objects.filter(name__icontains=status_query)

    wholesalers = Wholesaler.product_set.distinct().filter(Q(is_active__in=status_filter) & (Q(business_name__icontains=search_query) | Q(business_name__in=status_search)))

    return wholesalers, search_query