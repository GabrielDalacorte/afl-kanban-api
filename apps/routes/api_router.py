from rest_framework.routers import DefaultRouter, SimpleRouter
from django.conf import settings
from apps.users.api.viewsets import UserViewSet
from apps.kanban.api.viewsets import (
    BoardViewSet,
    ColumnViewSet,
    CardViewSet
)
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'boards', BoardViewSet, basename='board')
router.register(r'columns', ColumnViewSet, basename='column')
router.register(r'cards', CardViewSet, basename='card')

urlpatterns = router.urls + []