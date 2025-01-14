from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout




def login_user(request, redirect_page, template_name, context):
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

    
    return render(request, template_name, context)



def logout_user(request, redirect_page):
    logout(request)
    return redirect(redirect_page)