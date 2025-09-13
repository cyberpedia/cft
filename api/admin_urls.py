# api/admin_urls.py
from rest_framework.routers import DefaultRouter
from .admin_views import UserManagementViewSet, TeamManagementViewSet, TagManagementViewSet, ChallengeManagementViewSet, ContentPageManagementViewSet

router = DefaultRouter()
router.register(r'users', UserManagementViewSet)
router.register(r'teams', TeamManagementViewSet)
router.register(r'tags', TagManagementViewSet)
router.register(r'challenges', ChallengeManagementViewSet)
router.register(r'content-pages', ContentPageManagementViewSet)


urlpatterns = router.urls
