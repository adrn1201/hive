from django.shortcuts import render
from .forms import CustomUserCreationForm

def create_wholesalers(request):
    form = CustomUserCreationForm()
    context = {'form':form}
    return render(request, "wholesalers/create_wholesalers.html", context)



