from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

jwt_urlpatterns = [
    path("", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", include(jwt_urlpatterns)),
    path("auth/", include("customer.urls")),
    path("api/", include("dealership.urls")),
    path("api/", include("dealer.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    from django.urls import re_path

    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]

urlpatterns += doc_urls
