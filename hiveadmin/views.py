from django.shortcuts import render, redirect
from wholesalers.models import Wholesaler
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


def dashboard(request):
    return render(request, 'hiveadmin/dashboard.html')


def list_wholesalers(request):
    wholesalers = Wholesaler.objects.exclude(id=1).filter(is_active=True)
    context = {'wholesalers': wholesalers}

    if(request.method == "POST"):
        send_mail(
            'Hive Account Registration',
            'Please click the link to register your account http://localhost:8000/wholesalers/register',
            settings.EMAIL_HOST_USER,
            [request.POST['email']],
            fail_silently=False
        )
        messages.success(request, 'Registration has been successfully sent!')
        return redirect('list_wholesalers')
    return render(request, 'hiveadmin/wholesalers_list.html',context)


def transactions(request):
    return render(request, 'hiveadmin/transactions.html')


def admins(request):
    return render(request, 'hiveadmin/list_admin.html')


def registration_logs (request):
    return render(request, 'hiveadmin/logs.html')


def update_wholesaler(request, pk):
    
    wholesaler = Wholesaler.objects.get(id=pk)
    
    
    if request.method == "POST":
    
        if wholesaler.is_active & wholesaler.user.is_active == False:
            wholesaler.is_active = True
            wholesaler.user.is_active = True
            wholesaler.user.save()
            wholesaler.save()
            
        
        elif wholesaler.is_active & wholesaler.user.is_active == True:
            wholesaler.is_active = False
            wholesaler.user.is_active = False
            wholesaler.user.save()
            wholesaler.save()


        messages.success(request, 'Account status successfully updated!') 
        return redirect('list_wholesalers')
    context = {"wholesaler":wholesaler}
    return render(request, 'hiveadmin/wholesalers_list.html',context)
        

      
