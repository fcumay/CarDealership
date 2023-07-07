from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", views.LoginView.as_view(), name="login_view"),
    path(
        "register/",
        views.RegisterCustomerView.as_view(),
        name="register_customer"),
    path("customer/", views.CustomerView.as_view(), name="customer"),
    path(
        "dealership_admin/",
        views.DealershipAdminView.as_view(),
        name="dealership_admin",
    ),
    path("auth/user/register", views.RegisterViewAPI.as_view()),
]
