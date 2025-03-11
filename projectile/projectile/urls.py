from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/user", include("core.rest.urls.user")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/product", include("product.rest.urls.product")),
    path("api/v1/cart", include("cart.rest.urls.cart")),
] + debug_toolbar_urls()
