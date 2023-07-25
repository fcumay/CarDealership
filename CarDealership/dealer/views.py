from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from dealer.filters import (
    DealerFilter,
    DealerInventoryFilter,
    BuyingHistoryDealerFilter,
    PromotionDealershipFilter,
    PromotionDealerFilter,
)
from dealer.models import (
    Dealer,
    DealerInventory,
    BuyingHistoryDealer,
    PromotionDealership,
    PromotionDealer,
)

from dealer.serializers import (
    DealerSerializer,
    DealerInventorySerializer,
    BuyingHistoryDealerSerializer,
    PromotionDealershipSerializer,
    PromotionDealerSerializer,
)
from dealer.permissions import (
    IsAdminOrReadOnly,
    CanModifyDealer,
    IsAdminOwnerOrReadlOnly,
)


class DealerViewSet(viewsets.ModelViewSet):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DealerFilter
    permission_classes = [CanModifyDealer]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        if not (self.request.user.is_superuser):
            queryset = queryset.order_by("-created_at").filter(is_active=True)
        return queryset


class DealerInventoryViewSet(viewsets.ModelViewSet):
    queryset = DealerInventory.objects.all()
    serializer_class = DealerInventorySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DealerInventoryFilter
    permission_classes = [CanModifyDealer]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        if not (self.request.user.is_superuser):
            queryset = queryset.order_by("-created_at").filter(is_active=True)
        return queryset


class BuyingHistoryDealerViewSet(viewsets.ModelViewSet):
    queryset = BuyingHistoryDealer.objects.all()
    serializer_class = BuyingHistoryDealerSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BuyingHistoryDealerFilter
    permission_classes = [CanModifyDealer]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by("-created_at")
        return queryset


class PromotionDealershipViewSet(viewsets.ModelViewSet):
    queryset = PromotionDealership.objects.all()
    serializer_class = PromotionDealershipSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PromotionDealershipFilter
    permission_classes = [IsAdminOwnerOrReadlOnly]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by("-id")
        return queryset


class PromotionDealerViewSet(viewsets.ModelViewSet):
    queryset = PromotionDealer.objects.all()
    serializer_class = PromotionDealerSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PromotionDealerFilter
    permission_classes = [CanModifyDealer]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by("-id")
        return queryset
