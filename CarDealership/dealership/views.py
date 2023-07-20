from rest_framework import viewsets
from .filters import DealershipFilter
from .models import (
    Dealership,
)
from .serializers import (
    DealershipSerializer,
)
from .permissions import CanModifyDealership
from django_filters.rest_framework import DjangoFilterBackend

class DealershipViewSet(viewsets.ModelViewSet):
    queryset = Dealership.objects.all()
    serializer_class = DealershipSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class=DealershipFilter
    permission_classes = [CanModifyDealership]
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

