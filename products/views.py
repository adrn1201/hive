from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .forms import ProductForm, CategoryForm, VariationForm
from .utils import search_products, paginate_products
from django_tenants.utils import remove_www
from wholesalers.models import Domain, Wholesaler
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Variation

product_object = ''
@login_required(login_url='login_wholesaler')
def index(request):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    products, search_query = search_products(request)
    custom_range, products = paginate_products(request, products, 10)
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
    form = ProductForm(request.POST, request.FILES)
    variation_form = VariationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid() and request.POST['with_variation'] == '0':
            min_orders = form.cleaned_data['min_orders']
            actual_stocks = form.cleaned_data['actual_stocks']
            product = form.save(commit=False)
            product.wholesaler = wholesaler
            product.tempo_stocks = product.actual_stocks
            if min_orders >= actual_stocks:
                form.add_error('min_orders','Minimum order should be less than quantity')
            else:
                product.save()
                messages.success(request, 'Product has been successfully added')
                return redirect('products')
        elif (form.is_valid() and request.POST['with_variation'] == '1'): 
        
            if variation_form.is_valid():
                min_orders = form.cleaned_data['min_orders']
                var_stocks = variation_form.cleaned_data['actual_stocks_var']
                
                if min_orders >= var_stocks:
                    form.add_error('min_orders','Minimum order should be less than quantity')
                    
                else: 
                    print(request.POST)
                    product = form.save(commit=False)
                    product.wholesaler = wholesaler
                    product.save() 
            
                    for i in range(len(request.POST.getlist('name'))):                
                            Variation.objects.create(
                                product=product,
                                name=request.POST.getlist('name')[i],
                                actual_stocks_var=int(request.POST.getlist('actual_stocks_var')[i]),
                                tempo_stocks_var=int(request.POST.getlist('actual_stocks_var')[i])
                            )
                    messages.success(request, 'Product has been successfully added') 
                    return redirect('products')
            
            
           
    
    context = {"form":form, 'variation_form':variation_form}

    return render(request, "products/product_form.html", context)


def create_size_form(request):
    context = {'form':VariationForm()}
    return render(request, 'partials/size_form.html', context)


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
    product = wholesaler.product_set.get(id=pk)
    
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
    product = wholesaler.product_set.get(id=pk)
    
    form = ProductForm(instance=product)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            min_orders = form.cleaned_data['min_orders']
            actual_stocks = form.cleaned_data['actual_stocks']
            product = form.save(commit=False)
            product.tempo_stocks = product.actual_stocks
            if min_orders >= actual_stocks:
                form.add_error('min_orders','Minimum order should be less than quantity')
            else:
                product.save()
                messages.success(request, 'Product details has been successfully updated')
                return redirect('products')
            
    context = {"form":form, 'product_variation':[product.with_variation], 'edit_page' : True, 'product':product}
    return render(request, "products/edit_product.html", context)


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
    product = wholesaler.product_set.get(id=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product record successfully deleted!')
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
    products = category.product_set.all()
    product_count = category.product_set.all().count()
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
            messages.success(request, 'Category record successfully created!')
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
            messages.success(request, 'Category record successfully updated!')
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
        messages.success(request, 'Category record successfully deleted!')
        return redirect('categories')
    
    context = {"category":category}
    return render(request, "products/category_delete.html", context)


@login_required(login_url='login_wholesaler')
def display_sizes(request, pk):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    product = wholesaler.product_set.get(id=pk)
    
    variations = product.variation_set.all()
    context = {'variations': variations, 'product':product}
    return render(request, 'sizes/sizes.html', context)
    

@login_required(login_url='login_wholesaler')
def create_size(request, pk):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    
    product = wholesaler.product_set.get(id=pk)
    variation_form = VariationForm(request.POST or None)

    if variation_form.is_valid():
        for i in range(len(request.POST.getlist('name'))):                
            Variation.objects.create(
                product=product,
                name=request.POST.getlist('name')[i],
                actual_stocks_var=int(request.POST.getlist('actual_stocks_var')[i]),
                tempo_stocks_var=int(request.POST.getlist('actual_stocks_var')[i])
            )
        messages.success(request, 'Variation record successfully created!')
        return redirect('display_sizes', pk=product.id)
    
    context = {'form':variation_form, 'product':product}
    return render(request, 'sizes/form_size.html', context)


@login_required(login_url='login_wholesaler')
def edit_size(request, pk, size_pk):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    product = wholesaler.product_set.get(id=pk)
    variation = product.variation_set.get(id=size_pk)
    variation_form = VariationForm(request.POST or None, instance=variation)

    if request.method == "POST":
        if variation_form.is_valid():
            variation_data = variation_form.save(commit=False)
            variation_data.tempo_stocks_var = variation_data.actual_stocks_var
            variation_data.save()
            messages.success(request, 'Variation record successfully updated!')
            return redirect('display_sizes', pk=product.id)
    
    context = {"form":variation_form,'product':product, 'no_btns':True}
    return render(request, 'sizes/form_size.html', context)


@login_required(login_url='login_wholesaler')
def delete_size(request, pk, size_pk):
    try:
        request.user.wholesaler
    except:
        return HttpResponseForbidden()
    
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    wholesaler_id = domain.tenant.id
    wholesaler = Wholesaler.objects.get(id=wholesaler_id)
    product = wholesaler.product_set.get(id=pk)
    variation = product.variation_set.get(id=size_pk)
    
    if request.method == 'POST':
        variation.delete()
    messages.success(request, 'Variation record successfully deleted!')
    return redirect('display_sizes', pk=product.id)
