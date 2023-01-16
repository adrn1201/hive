from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="products"),
    path('new/', views.create_product, name="create-product"),

    #View details for product
    path('<str:pk>/', views.view_product, name="view-product"),

    #Delete a Product
    path('<str:pk>/delete/', views.delete_product, name="delete-product"),

]