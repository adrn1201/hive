from django.shortcuts import render, redirect



def index(request):
    # Display all products
    return render(request, "retailers/retailers.html")