from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    path("admin/", admin.site.urls),
    path("", include("w_dashboard.urls")),
    path("account/", include("account.urls")),
    path("products/", include("products.urls")),
    path("shop/", include("shop.urls")),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("transactions/", include("transactions.urls")),
    path("analytics/", include("analytics.urls")),
    path("retailers/", include("retailers.urls")),
    path("wholesalers/", include("wholesalers.urls")),
    path("hiveadmin/", include("hiveadmin.urls")),
   

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

