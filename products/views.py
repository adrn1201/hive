from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .forms import InventoryForm, CategoryForm
from .utils import search_products, paginate_products
from django_tenants.utils import remove_www
from wholesalers.models import Domain, Wholesaler
from django.contrib.auth.decorators import login_required


@login_required(login_url='login_wholesaler')
def index(request):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    products, search_query = search_products(request)
    custom_range, products = paginate_products(request, products, 15)
    context = {'products': products, 'search_query': search_query, 'custom_range':custom_range}
    return render(request, "products/index.html", context)


@login_required(login_url='login_wholesaler')
def create_product(request):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
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


@login_required(login_url='login_wholesaler')
def view_product(request, pk):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    product = wholesaler.inventory_set.get(id=pk)
    
    context ={'product':product}
    return render(request, "products/view_product.html", context)


@login_required(login_url='login_wholesaler')
def edit_product(request, pk):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
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


@login_required(login_url='login_wholesaler')
def delete_product(request, pk):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
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


@login_required(login_url='login_wholesaler')
def show_categories(request):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    categories = wholesaler.category_set.filter(wholesaler=wholesaler)
    
    context = {"categories":categories}
    return render(request, "products/categories.html", context)


@login_required(login_url='login_wholesaler')
def show_category(request, pk):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    
    category = wholesaler.category_set.get(id=pk)
    products = category.inventory_set.all()
    product_count = category.inventory_set.all().count()
    context = {"category":category, "product_count":product_count, "products":products}
    return render(request, "products/category_detail.html", context)


@login_required(login_url='login_wholesaler')
def create_category(request):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
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


@login_required(login_url='login_wholesaler')
def edit_category(request, pk):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
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


@login_required(login_url='login_wholesaler')
def delete_category(request, pk):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
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

