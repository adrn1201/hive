from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name="retailers"),
    path('register/', views.register_retailer, name='register_retailer'),
    path('profile/', views.retailer_create_profile, name='retailer_create_profile'),
    path('dashboard/', views.dashboard_retailer, name='dashboard_retailer'),
    path('profile/edit/', views.retailer_edit_profile, name='retailer_edit_profile'),
]