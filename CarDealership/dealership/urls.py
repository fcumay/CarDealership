from django.urls import path
from .views import (
    ManageDealershipView,
    ManageBrandView,
    ManageModelView,
    ManageCarView,
)

urlpatterns = [
    path("dealership/manage/", ManageDealershipView.as_view()),
    path("brand/manage/", ManageBrandView.as_view()),
    path("model/manage/", ManageModelView.as_view()),
    path("car/manage/", ManageCarView.as_view()),
]
