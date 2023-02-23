from django.shortcuts import render, redirect
from wholesalers.models import Wholesaler
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


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


def list_deac(request):

    wholesalers = Wholesaler.objects.filter(is_active=False)
    context = {'wholesalers': wholesalers}
    return render(request, 'hiveadmin/wholesalers_deac.html',context)


def update_wholesaler(request, pk):
    
    retailer = Wholesaler.objects.get(id=pk)
    
    
    if request.method == "POST":
    
        if retailer.is_active & retailer.user.is_active == False:
            retailer.is_active = True
            retailer.user.is_active = True
            retailer.user.save()
            retailer.save()
            
        
        elif retailer.is_active & retailer.user.is_active == True:
            retailer.is_active = False
            retailer.user.is_active = False
            retailer.user.save()
            retailer.save()


        messages.success(request, 'Account status successfully updated!') 
        return redirect('list_wholesalers')
    context = {"retailer":retailer}
    return render(request, 'hiveadmin/wholesalers_list.html',context)
        

      
