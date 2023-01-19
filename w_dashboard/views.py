from django.shortcuts import render

def w_dashboard(request):
    return render(request, 'w_dashboard/dashboard.html')
