from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_wholesalers, name="list_wholesalers"),
    path('<int:pk>', views.update_wholesaler, name='update_wholesaler'),
    path('inactive/', views.list_deac, name="list_deac"),

]