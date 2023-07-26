from django.urls import path, include
from .views import UserViewSet, BuyingHistoryCustomerViewSet, InformationViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"info", InformationViewSet, basename="info")
router.register(r"history", BuyingHistoryCustomerViewSet, basename="history")

urlpatterns = [
    path("", include(router.urls)),
]
