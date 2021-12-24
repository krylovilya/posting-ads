from rest_framework.routers import DefaultRouter

from apps.api.viewsets import AdViewSet

router = DefaultRouter()
router.register('ad', AdViewSet, basename='ad')
