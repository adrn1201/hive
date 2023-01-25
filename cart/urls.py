from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_cart, name="show_cart"),
    path('add/', views.cart_add, name='cart_add'),

]