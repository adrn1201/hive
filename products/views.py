from django.shortcuts import render, redirect
from .models import Inventory, Category
from .forms import InventoryForm, CategoryForm
from django_tenants.utils import remove_www
from wholesalers.models import Domain, Wholesaler


def index(request):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    products = wholesaler.inventory_set.filter(wholesaler=wholesaler)
    context = {"products":products}
    return render(request, "products/index.html", context)


def create_product(request):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    form = InventoryForm()
    
    if request.method == "POST":
        form = InventoryForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.tempo_quantity = product.actual_quantity
            product.wholesaler = wholesaler
            product.save()
            return redirect('products')
    
    context = {"form":form}
    return render(request, "products/product_form.html", context)


def view_product(request, pk):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    product = wholesaler.inventory_set.get(id=pk)
    
    context ={'product':product}
    return render(request, "products/view_product.html", context)


def edit_product(request, pk):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    product = wholesaler.inventory_set.get(id=pk)
    
    form = InventoryForm(instance=product) 

    if request.method == "POST":
        form = InventoryForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    
    context = {"form":form}
    return render(request, "products/product_form.html", context)


def delete_product(request, pk):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    product = wholesaler.inventory_set.get(id=pk)
    
    if request.method == 'POST':
        product.delete()
        return redirect("products")
    context={'product':product}
    return render(request, "products/delete_product.html", context)


def show_categories(request):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    categories = wholesaler.category_set.filter(wholesaler=wholesaler)
    
    context = {"categories":categories}
    return render(request, "products/categories.html", context)


def show_category(request, pk):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    
    category = wholesaler.category_set.get(id=pk)
    products = category.inventory_set.all()
    product_count = category.inventory_set.all().count()
    context = {"category":category, "product_count":product_count, "products":products}
    return render(request, "products/category_detail.html", context)


def create_category(request):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    form = CategoryForm()
    
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.wholesaler = wholesaler
            category.save()
            return redirect('categories')
    
    context = {"form":form}
    return render(request, "products/category_form.html", context)


def edit_category(request, pk):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    category = wholesaler.category_set.get(id=pk)
    form = CategoryForm(instance=category)
    
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    
    context = {"form":form}
    return render(request, "products/category_form.html", context)


def delete_category(request, pk):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    category = wholesaler.category_set.get(id=pk)
    
    if request.method == "POST":
        category.delete()
        return redirect('categories')
    
    context = {"category":category}
    return render(request, "products/category_delete.html", context)

