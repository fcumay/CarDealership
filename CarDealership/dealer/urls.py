from django.urls import path
from .views import (
    ManageDealerView,
    ManageDealerInventoryView,
)

urlpatterns = [
    path("dealer/manage/", ManageDealerView.as_view()),
    path("inventory/manage/", ManageDealerInventoryView.as_view()),
]
