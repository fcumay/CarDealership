from django.urls import path, include
from .views import (
    DealerViewSet,
    DealerInventoryViewSet,
    BuyingHistoryDealerViewSet,
    PromotionDealershipViewSet,
    PromotionDealerViewSet,
)

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"dealer", DealerViewSet, basename="dealer")
router.register(r"inventory", DealerInventoryViewSet, basename="inventory")
router.register(r"history", BuyingHistoryDealerViewSet, basename="history")
router.register(
    r"promotiondealership", PromotionDealershipViewSet, basename="promotiondealership"
)
router.register(
    r"promotiondealer", PromotionDealershipViewSet, basename="promotiondealer"
)

urlpatterns = [
    path("", include(router.urls)),
]
