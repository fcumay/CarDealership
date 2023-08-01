from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

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


class DealerViewSet(viewsets.ModelViewSet):
    serializer_class = DealerSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DealerFilter
    permission_classes = [CanModifyDealer]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = Dealer.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(is_active=True).order_by("-created_at")
        return queryset


class DealerInventoryViewSet(viewsets.ModelViewSet):
    serializer_class = DealerInventorySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DealerInventoryFilter
    permission_classes = [CanModifyDealer]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = DealerInventory.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(is_active=True).order_by("-created_at")
        return queryset


class BuyingHistoryDealerViewSet(viewsets.ModelViewSet):
    serializer_class = BuyingHistoryDealerSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BuyingHistoryDealerFilter
    permission_classes = [CanModifyDealer]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = BuyingHistoryDealer.objects.all()
        queryset = queryset.order_by("-created_at")
        return queryset


class PromotionDealershipViewSet(viewsets.ModelViewSet):
    serializer_class = PromotionDealershipSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PromotionDealershipFilter
    permission_classes = [IsAdminOwnerOrReadlOnly]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = PromotionDealership.objects.all()
        queryset = queryset.order_by("-id")
        return queryset


class PromotionDealerViewSet(viewsets.ModelViewSet):
    serializer_class = PromotionDealerSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PromotionDealerFilter
    permission_classes = [CanModifyDealer]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = PromotionDealer.objects.all()
        queryset = queryset.order_by("-id")
        return queryset
