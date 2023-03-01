from django.urls import path
from . import views


urlpatterns = [

    path('register/', views.register_admin, name='register_admin'),
    path('login/', views.login_admin, name='login_admin'),
    path('logout/', views.logout_admin, name="logout_admin"),

    path('', views.dashboard, name="dashboard"),
    path('wholesalers/', views.list_wholesalers, name="list_wholesalers"),
    path('<int:pk>', views.update_wholesaler, name='update_wholesaler'),
    path('transactions/', views.transactions, name='transactions'),
    path('admin/', views.admins, name='admins'),
    path('logs/', views.registration_logs, name='registration_logs'),
]