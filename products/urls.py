from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="products"),
    path('new/', views.create_product, name="create-product"),

]