from django.contrib import admin
from .models import Category, Inventory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    
    
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'product_name', 'actual_quantity']
