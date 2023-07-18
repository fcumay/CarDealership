from django.urls import path
from .views import RetrieveUserView, RegisterViewAPI, BuyingHistoryCustomerView

urlpatterns = [
    path("register", RegisterViewAPI.as_view()),
    path("me", RetrieveUserView.as_view()),
    path("history/manage", BuyingHistoryCustomerView.as_view()),
]
