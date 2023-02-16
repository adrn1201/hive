from django.shortcuts import render, redirect
from wholesalers.models import Wholesaler
from django.core.mail import send_mail
from django.conf import settings
from wholesalers.forms import WholesalerCreationForm


def list_wholesalers(request):

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
        return redirect('list_wholesalers')
    return render(request, 'hiveadmin/wholesalers_list.html',context)


def list_deac(request):

    wholesalers = Wholesaler.objects.filter(is_active=False)
    context = {'wholesalers': wholesalers}
    return render(request, 'hiveadmin/wholesalers_deac.html',context)


def deactivate_acc (request,pk):

    if (request.method == "POST"):

        wholesalers = Wholesaler.objects.get(id=pk)
        wholesalers.is_active = False
        wholesalers.save()
        context = {'wholesalers': wholesalers}
        return redirect('list_wholesalers')
    return render(request, 'hiveadmin/wholesalers_list.html',context)
        

      
