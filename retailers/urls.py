from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', views.index, name="retailers"),
    path('register/', views.register_retailer, name='register_retailer'),
    path('profile/', views.retailer_create_profile, name='retailer_create_profile'),
    path('dashboard/', views.dashboard_retailer, name='dashboard_retailer'),
    path('dashboard/order-product/<int:pk>/', views.order_items, name='ordered_product'),
    path('aboutus/', views.about_us, name='about_us'),
    path('profile/view/', views.retailer_view_profile, name='retailer_view_profile'),
    path('profile/edit/', views.retailer_edit_profile, name='retailer_edit_profile'),
    path('<int:pk>',views.deactivate_retailer, name='deactivate_retailer'),
]
# ?P<pk>\d+)/$
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)