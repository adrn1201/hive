from django.shortcuts import render, redirect
from wholesalers.models import Wholesaler
from django.core.mail import send_mail
from django.conf import settings


def list_wholesalers(request):

    if not request.user.is_superuser and (
            request.user.wholesaler.is_wholesaler or request.user.wholesaler.is_retailer):
    
        return redirect('w_dashboard')
    wholesalers = Wholesaler.objects.filter(is_active=True)
    context = {'wholesalers': wholesalers}

    if(request.method == "POST"):
        send_mail(
            'Hive Account Registration',
            'Please click the link to register your account http://localhost:8000/wholesalers/register',
            settings.EMAIL_HOST_USER,
            [request.POST['email']],
            fail_silently=False
        )
        return redirect('products')
    return render(request, 'hiveadmin/wholesalers_list.html',context)



      
