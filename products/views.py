from django.shortcuts import render, redirect
from .models import Inventory, Category
from .forms import InventoryForm, CategoryForm


def index(request):
    # Display all products
    products = Inventory.objects.all() 
    context = {"products":products}
    return render(request, "main.html", context)


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


def edit_product(request, pk):
    product = Inventory.objects.get(id=pk)
    form = InventoryForm(instance=product) 

    if request.method == "POST":
        form = InventoryForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            #save to database
            form.save()
            return redirect('products')
    
    context = {"form":form}
    return render(request, "products/product_form.html", context)


def delete_product(request, pk):
    product = Inventory.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect("products")
    context={'product':product}
    return render(request, "products/delete_product.html", context)


def show_categories(request):
    categories = Category.objects.all()
    
    

    context = {"categories":categories}
    return render(request, "products/categories.html", context)


def show_category(request, pk):
    category = Category.objects.get(id=pk)
    
    products = category.inventory_set.all()
    product_count = category.inventory_set.all().count()
    context = {"category":category, "product_count":product_count, "products":products}
    return render(request, "products/category_detail.html", context)


def create_category(request):
    form = CategoryForm()
    
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    
    context = {"form":form}
    return render(request, "products/category_form.html", context)


def edit_category(request, pk):
    category = Category.objects.get(id=pk)
    form = CategoryForm(instance=category)
    
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    
    context = {"form":form}
    return render(request, "products/category_form.html", context)


def delete_category(request, pk):
    category = Category.objects.get(id=pk)
    
    if request.method == "POST":
        category.delete()
        return redirect('categories')
    
    context = {"category":category}
    return render(request, "products/category_delete.html", context)

