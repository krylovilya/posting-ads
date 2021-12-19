from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from apps.api.permissions import UserIsObjectOwnerPermission
from apps.api.serializers import AdSerializer
from apps.main.models import Ad


class AdViewSet(ModelViewSet):
    """CRUD операции над объявлениями."""

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (permissions.IsAuthenticated, UserIsObjectOwnerPermission)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.seller)
