from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="products"),
    path('new/', views.create_product, name="create-product"),

    #View details for product
    path('<str:pk>/', views.view_product, name="view-product"),

    #Edit a product
    path('<str:pk>/edit/', views.edit_product, name="edit-product"),

    #Delete a Product
    path('<str:pk>/delete/', views.delete_product, name="delete-product"),

]