from rest_framework import viewsets
from .filters import DealershipFilter, BrandFilter, ModelFilter, CarFilter
from .models import Model, Brand, Car, Dealership
from .serializers import (
    DealershipSerializer,
    BrandSerializer,
    ModelSerializer,
    CarSerializer,
)
from .permissions import CanModifyDealership, IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class DealershipViewSet(viewsets.ModelViewSet):
    serializer_class = DealershipSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DealershipFilter
    permission_classes = [CanModifyDealership]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = Dealership.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(is_active=True).order_by("-created_at")
        return queryset


class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BrandFilter
    permission_classes = [IsAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = Brand.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(is_active=True).order_by("-created_at")
        return queryset


class ModelViewSet(viewsets.ModelViewSet):
    serializer_class = ModelSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ModelFilter
    permission_classes = [IsAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = Model.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(is_active=True).order_by("-created_at")
        return queryset


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CarFilter
    permission_classes = [IsAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = Car.objects.all()
        if not self.request.user.is_superuser:
            queryset = (
                queryset.filter(customer=None)
                .exclude(is_active=False).order_by("-created_at")
            )
        return queryset
