from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_wholesalers, name="list_wholesalers"),
    path('<int:pk>/', views.deactivate_acc, name="deac_acc"),
    path('inactive/', views.list_deac, name="list_deac"),

]