from rest_framework import viewsets
from .filters import DealershipFilter, BrandFilter, ModelFilter, CarFilter
from .models import (
    Dealership,
    Brand,
    Model,
    Car,
)
from .serializers import (
    DealershipSerializer,
    BrandSerializer,
    ModelSerializer,
    CarSerializer,
)
from .permissions import CanModifyDealership, IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class DealershipViewSet(viewsets.ModelViewSet):
    queryset = Dealership.objects.all()
    serializer_class = DealershipSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DealershipFilter
    permission_classes = [CanModifyDealership]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        if not (self.request.user.is_superuser):
            queryset = queryset.order_by("-created_at").filter(is_active=True)
        return queryset


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BrandFilter
    permission_classes = [IsAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        if not (self.request.user.is_superuser):
            queryset = queryset.order_by("-created_at").filter(is_active=True)
        return queryset


class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ModelFilter
    permission_classes = [IsAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        if not (self.request.user.is_superuser):
            queryset = queryset.order_by("-created_at").filter(is_active=True)
        return queryset


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CarFilter
    permission_classes = [IsAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        if not (self.request.user.is_superuser):
            queryset = (
                queryset.order_by("-created_at")
                .filter(customer=None)
                .exclude(is_active=False)
            )
        return queryset
