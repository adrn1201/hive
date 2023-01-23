from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_shop, name="show_shop"),

]