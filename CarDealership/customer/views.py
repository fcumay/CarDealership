from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .filters import UserFilter
from .models import Customer, BuyingHistoryCustomer
from rest_framework import status, viewsets
from django.contrib.auth import get_user_model
from .permissions import RegistrationPermission, Information
from .serializers import (
    UserSerializer,
    BuyingHistoryCustomerSerializer,
    InformationSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter
    permission_classes = (RegistrationPermission,)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by("-id")
        return queryset

    def perform_create(self, serializer):
        if (
            self.request.data.get("role") == "dealership_admin"
            and not self.request.user.is_superuser
        ):
            raise PermissionDenied(
                "Only superuser can create dealership_admin user")
        return super().perform_create(serializer)


class InformationViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = InformationSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (Information,)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by("-id")
        return queryset


class BuyingHistoryCustomerViewSet(viewsets.ModelViewSet):
    queryset = BuyingHistoryCustomer.objects.all()
    serializer_class = BuyingHistoryCustomerSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(customer=self.request.user)
        return queryset
