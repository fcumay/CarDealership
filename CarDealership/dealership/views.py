from rest_framework.response import Response
from .models import (
    Dealership,
)
from .serializers import (
    DealershipSerializer,
)
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .permissions import CanModifyDealership
from rest_framework import mixins, generics


class ManageDealershipView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView

):
    queryset = Dealership.objects.all()
    serializer_class = DealershipSerializer
    permission_classes = [CanModifyDealership]
    lookup_field = 'name'

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        allowed_objects = []
        for obj in queryset:
            try:
                self.check_object_permissions(self.request, obj)
                allowed_objects.append(obj)
            except:
                continue
        return Dealership.objects.filter(id__in=[obj.id for obj in allowed_objects])

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()

        if not request.user.is_superuser and ('balance' in request.data or 'owner' in request.data):
            return Response({'detail': 'You are not allowed to modify balance or owner.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


