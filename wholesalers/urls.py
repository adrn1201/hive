from django.urls import path
from . import views


urlpatterns = [
    path('', views.email_wholesaler, name="email_wholesalers"),
    path('register/', views.register_wholesalers, name="register_wholesalers"),
    path('profile/', views.wholesaler_profile, name="profile_wholesalers"),
]