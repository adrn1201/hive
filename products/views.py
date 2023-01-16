from django.shortcuts import render, redirect
from .models import Inventory
from .forms import InventoryForm


def index(request):
    # Display all products
    products = Inventory.objects.all() 
    context = {"products":products}
    return render(request, "products/index.html", context)


def create_product(request):
    #Process form Data
    form = InventoryForm()
    
    if request.method == "POST":
        form = InventoryForm(request.POST, request.FILES)
        if form.is_valid():
            #save to database
            form.save()
            return redirect('products')
    
    context = {"form":form}
    return render(request, "products/product_form.html", context)

def view_product(request, pk):

    product = Inventory.objects.get(id=pk)

    context ={'product':product}
    return render(request, "products/view_product.html", context)

def delete_product(request, pk):
    product = Inventory.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect("products")
    context={'product':product}
    return render(request, "products/delete_product.html", context)


