from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from customer.views import DeactivationMixin
from dealer.filters import (
    DealerFilter,
    DealerInventoryFilter,
    BuyingHistoryDealerFilter,
    PromotionDealershipFilter,
    PromotionDealerFilter,
)
from dealer.models import Dealer, DealerInventory, BuyingHistoryDealer, PromotionDealership, PromotionDealer

from dealer.serializers import (
    DealerSerializer,
    DealerInventorySerializer,
    BuyingHistoryDealerSerializer,
    PromotionDealershipSerializer,
    PromotionDealerSerializer,
)
from dealer.permissions import (
    CanModifyDealer,
    IsAdminOwnerOrReadlOnly,
)


class DealerViewSet(DeactivationMixin, viewsets.ModelViewSet):
    serializer_class = DealerSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DealerFilter
    permission_classes = [CanModifyDealer]

    def get_queryset(self):
        queryset = Dealer.objects.all()
        if not self.request.user.is_superuser:
            return queryset.filter(is_active=True).order_by("-created_at")
        return queryset


class DealerInventoryViewSet(DeactivationMixin, viewsets.ModelViewSet):
    serializer_class = DealerInventorySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DealerInventoryFilter
    permission_classes = [CanModifyDealer]

    def get_queryset(self):
        queryset = DealerInventory.objects.all()
        if not self.request.user.is_superuser:
            return queryset.filter(is_active=True).order_by("-created_at")
        return queryset


class BuyingHistoryDealerViewSet(DeactivationMixin, viewsets.ModelViewSet):
    serializer_class = BuyingHistoryDealerSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BuyingHistoryDealerFilter
    permission_classes = [CanModifyDealer]

    def get_queryset(self):
        return BuyingHistoryDealer.objects.all().order_by("-created_at")


class PromotionDealershipViewSet(DeactivationMixin, viewsets.ModelViewSet):
    serializer_class = PromotionDealershipSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PromotionDealershipFilter
    permission_classes = [IsAdminOwnerOrReadlOnly]

    def get_queryset(self):
        return PromotionDealership.objects.all().order_by("-id")


class PromotionDealerViewSet(DeactivationMixin, viewsets.ModelViewSet):
    serializer_class = PromotionDealerSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PromotionDealerFilter
    permission_classes = [CanModifyDealer]

    def get_queryset(self):
        return PromotionDealer.objects.all().order_by("-id")
