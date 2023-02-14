from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_orders, name="display_orders"),
    path('create/', views.create_order, name="create_order"),
]