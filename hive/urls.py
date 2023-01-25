from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("w_dashboard.urls")),
    path("products/", include("products.urls")),
    path("shop/", include("shop.urls")),
      path("cart/", include("cart.urls")),
    path("retailers/", include("retailers.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

