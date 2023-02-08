from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_wholesalers, name="list_wholesalers"),

]