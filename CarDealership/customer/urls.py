from django.urls import path, include
from .views import UserViewSet, BuyingHistoryCustomerViewSet, InformationViewSet
from rest_framework import routers
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView

router = routers.DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"info", InformationViewSet, basename="info")
router.register(r"history", BuyingHistoryCustomerViewSet, basename="history")
urlpatterns = [
    path("", include(router.urls)),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("auth/password-reset-complete/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]
