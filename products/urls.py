from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="products"),
    path('new/', views.create_product, name="create-product"),
    path('categories/', views.show_categories, name="categories"),
    path('categories/new/', views.create_category, name="create-category"),

    #View details for product
    path('<str:pk>/', views.view_product, name="view-product"),

    #Edit a product
    path('<str:pk>/edit/', views.edit_product, name="edit-product"),

    #Delete a Product
    path('<str:pk>/delete/', views.delete_product, name="delete-product"),
    

    path('categories/<str:pk>/', views.show_category, name="show-category"),
    path('categories/<str:pk>/edit/', views.edit_category, name="edit-category"),
    path('categories/<str:pk>/delete/', views.delete_category, name="delete-category"),

]