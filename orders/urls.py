from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_orders, name="display_orders"),
    path('create/', views.create_order, name="create_order"),
    path('<int:pk>/', views.order_details, name="order_details"),
     path('sales/', views.sales_report, name="sales_report"),
    path('webhook/', views.stripe_webhook, name='stripe-webhook'),
    path('create-payment-intent/', views.stripe_intent, name='create-payment-intent')
]