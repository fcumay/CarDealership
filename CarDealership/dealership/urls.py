from django.urls import path, include
from .views import DealershipViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'dealership', DealershipViewSet,basename='dealership')

urlpatterns = [
    path('', include(router.urls)),
]
