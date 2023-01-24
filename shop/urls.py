from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_shop, name="show_shop"),
    path('<str:pk>/', views.view_item, name="view_item"),

]