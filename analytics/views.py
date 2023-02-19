from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django_tenants.utils import remove_www
from wholesalers.models import Domain, Wholesaler
from django.contrib.auth.decorators import login_required

@login_required(login_url='login_wholesaler')
def display_analytics(request):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    return render(request, 'analytics/forecasting.html')
