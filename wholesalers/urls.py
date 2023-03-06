from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register_wholesalers, name="register_wholesalers"),
    
    path('profile/', views.wholesaler_create_profile, name="wholesaler_create_profile"),
    path('edit-profile/', views.wholesaler_edit_profile, name="wholesaler_edit_profile"),
    path('view-profile/', views.wholesaler_view_profile, name='wholesaler_view_profile'),
    path('retailers/email/', views.email_retailer, name="email_retailer"),
    path('transactions/', views.transactions, name="transactions_wholesalers"),
    path('transactions/<int:pk>/', views.transaction_details, name="transaction_details"),
]