from rest_framework import viewsets
from rest_framework.decorators import action
from customer.views import DeactivationMixin
from dealership import utils
from .filters import DealershipFilter, BrandFilter, ModelFilter, CarFilter
from .models import Model, Brand, Car, Dealership
from .serializers import (
    DealershipSerializer,
    BrandSerializer,
    ModelSerializer,
    CarSerializer, OfferSerializer,
)
from .permissions import CanModifyDealership, IsAdminOrReadOnly, EmailConfirmPermission, CarPermission
from django_filters.rest_framework import DjangoFilterBackend
from dealership import tasks
from django.http import JsonResponse
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class DealershipViewSet(DeactivationMixin, viewsets.ModelViewSet):
    serializer_class = DealershipSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DealershipFilter
    permission_classes = [CanModifyDealership]

    def get_queryset(self):
        queryset = Dealership.objects.all()
        if not self.request.user.is_superuser:
            return queryset.filter(is_active=True).order_by("-created_at")
        return queryset

    @action(detail=False, methods=["GET"], url_path="statistic/(?P<id>\\d+)")
    def get_statistics(self, request, id):
        dealership = utils.get_dealership(id)
        return Response(utils.get_statistic(dealership))


class BrandViewSet(DeactivationMixin, viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BrandFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Brand.objects.all()
        if not self.request.user.is_superuser:
            return queryset.filter(is_active=True).order_by("-created_at")
        return queryset


class ModelViewSet(DeactivationMixin, viewsets.ModelViewSet):
    serializer_class = ModelSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ModelFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Model.objects.all()
        if not self.request.user.is_superuser:
            return queryset.filter(is_active=True).order_by("-created_at")
        return queryset


class CarViewSet(DeactivationMixin, viewsets.ModelViewSet):
    serializer_class = CarSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CarFilter
    permission_classes = [CarPermission]

    def get_queryset(self):
        queryset = Car.objects.all()
        if not self.request.user.is_superuser:
            return queryset.filter(customer=None).exclude(
                is_active=False).order_by("-created_at")
        return queryset


class OfferViewSet(viewsets.ViewSet):
    permission_classes = [EmailConfirmPermission]
    serializer_class = OfferSerializer

    @swagger_auto_schema(request_body=OfferSerializer)
    def create(self, request):
        if request.method == 'POST':
            user = request.user.id
            data = request.data.copy()
            tasks.do_offer.delay(user, data)
            return JsonResponse({'message': 'Offer task has been scheduled'})
        return JsonResponse({'message': 'Only POST requests are allowed'})
