from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_cart, name="show_cart"),
    path('add/', views.cart_add, name='cart_add'),
    path('remove/', views.cart_delete, name='cart_delete'),
    path('update/', views.cart_update, name='cart_update'),
]