from django.urls import path, include
from .views import DealershipViewSet, BrandViewSet, ModelViewSet, CarViewSet, OfferViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"dealership", DealershipViewSet, basename="dealership")
router.register(r"brand", BrandViewSet, basename="brand")
router.register(r"model", ModelViewSet, basename="model")
router.register(r"car", CarViewSet, basename="car")
router.register(r"offer", OfferViewSet, basename="offer")

urlpatterns = [
    path("", include(router.urls)),
]
