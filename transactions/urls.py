from django.urls import path
from . import views

urlpatterns = [
     path('', views.display_transactions, name="display_transactions"),
]