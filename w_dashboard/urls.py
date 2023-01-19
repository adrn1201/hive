from django.urls import path

from . import views
urlpatterns = [
    path("", views.w_dashboard, name="w_dashboard"),
]