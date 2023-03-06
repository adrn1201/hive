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
    path('wholesaler-logs/', views.wholesaler_activity_logs, name='wholesaler-logs'),
    path('retailer-logs/', views.retailer_activity_logs, name='retailer-logs'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success_payment, name='success_payment'),
    path('checkout-session/', views.checkout_session_payment, name='checkout_session_payment'),
    path('customer-portal/', views.customer_portal, name='customer_portal'),
    path('webhook/', views.webhook_received, name='webhook_received'),
    path('update-admin/<int:pk>', views.update_admin_status, name='update_admin_status'),
]