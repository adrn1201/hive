from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register_wholesalers, name="register_wholesalers"),
    
    path('profile/', views.wholesaler_create_profile, name="wholesaler_create_profile"),
    path('edit-profile/', views.wholesaler_edit_profile, name="wholesaler_edit_profile"),
    path('retailers/email/', views.email_retailer, name="email_retailer"),
]