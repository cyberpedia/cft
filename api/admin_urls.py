# api/admin_urls.py
from rest_framework.routers import DefaultRouter
from .admin_views import UserManagementViewSet, TeamManagementViewSet

router = DefaultRouter()
router.register(r'users', UserManagementViewSet)
router.register(r'teams', TeamManagementViewSet)

urlpatterns = router.urls
