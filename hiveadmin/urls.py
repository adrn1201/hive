from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_wholesalers, name="list_wholesalers"),
    path('register/', views.register_admin, name='register_admin'),
    path('login/', views.login_admin, name='login_admin'),
    path('<int:pk>', views.update_wholesaler, name='update_wholesaler'),
    path('logout/', views.logout_admin, name="logout_admin"),

]