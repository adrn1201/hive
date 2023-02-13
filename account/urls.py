from django.urls import path
from . import views



urlpatterns = [
    path('wholesalers/login/', views.login_wholesaler, name="login_wholesaler"),
    path('wholesalers/logout/', views.logout_wholesaler, name="logout_wholesaler"),
    
    path('retailers/login/', views.login_retailer, name="login_retailer"),
    path('retailers/logout/', views.logout_retailer, name="logout_retailer"),
]