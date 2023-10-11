from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from . import utils
from .filters import UserFilter
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .models import BuyingHistoryCustomer, Customer
from .permissions import RegistrationPermission, Information
from .serializers import (
    UserSerializer,
    BuyingHistoryCustomerSerializer,
    InformationSerializer,
)
from rest_framework import status

User = get_user_model()


class DeactivationMixin:
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class UserViewSet(DeactivationMixin, viewsets.ModelViewSet):
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter
    permission_classes = (RegistrationPermission,)

    def get_queryset(self):
        return User.objects.all().order_by("-id")

    def perform_create(self, serializer):
        if (
                self.request.data.get("role") == "dealership_admin"
                and not self.request.user.is_superuser
        ):
            raise PermissionDenied(
                "Only superuser can create dealership_admin user")
        user = serializer.save()
        token = utils.generate_verification_token()
        User.objects.set_email_verification_token(user, token)
        utils.send_email_link(token, user)

        return user

    @action(detail=False, methods=["GET"])
    def verify_email(self, request):
        token = request.GET.get("token")
        try:
            user = Customer.objects.get(email_verification_token=token)
            User.objects.verify_email(user)
            return Response(
                {"message": "Email verified successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise ValidationError("Invalid verification token.")

    @action(detail=False, methods=["POST"])
    def send_password_reset_link(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("User with this email does not exist.")
        utils.send_password_reset_link(user, email)
        return Response(
            {"message": "Password reset link sent successfully."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="statistic/(?P<id>\\d+)")
    def get_statistics(self, request, id):
        customer = utils.get_customer(id)
        return Response(utils.get_statistic(customer))


class InformationViewSet(viewsets.ModelViewSet):
    serializer_class = InformationSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (Information,)

    def get_queryset(self):
        return Customer.objects.all().order_by("-id")


class BuyingHistoryCustomerViewSet(DeactivationMixin, viewsets.ModelViewSet):
    serializer_class = BuyingHistoryCustomerSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return BuyingHistoryCustomer.objects.filter(
                customer=self.request.user).order_by("-created_at")
        else:
            return BuyingHistoryCustomer.objects.none()

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)
