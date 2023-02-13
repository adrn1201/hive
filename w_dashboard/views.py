from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


@login_required(login_url='login_wholesaler')
def w_dashboard(request):    
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    return render(request, 'w_dashboard/dashboard.html')
