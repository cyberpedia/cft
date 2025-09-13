# api/admin_views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import User, Team, Challenge, Tag, ContentPage
from .serializers import AdminUserSerializer, AdminTeamSerializer, AdminChallengeSerializer, AdminTagSerializer, ContentPageSerializer


class UserManagementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for administrators to manage user accounts.
    Provides CRUD operations for User model instances.
    Requires admin privileges.
    """
    queryset = User.objects.all().order_by('username')
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]


class TeamManagementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for administrators to manage teams.
    Provides CRUD operations for Team model instances.
    Requires admin privileges.
    """
    queryset = Team.objects.all().order_by('name')
    serializer_class = AdminTeamSerializer
    permission_classes = [IsAdminUser]


class TagManagementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for administrators to manage challenge tags.
    Provides CRUD operations for Tag model instances.
    Requires admin privileges.
    """
    queryset = Tag.objects.all().order_by('name')
    serializer_class = AdminTagSerializer
    permission_classes = [IsAdminUser]


class ChallengeManagementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for administrators to manage challenges.
    Provides CRUD operations for Challenge model instances, including flag and all scoring details.
    Requires admin privileges.
    """
    queryset = Challenge.objects.all().order_by('name')
    serializer_class = AdminChallengeSerializer
    permission_classes = [IsAdminUser]


class ContentPageManagementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for administrators to manage content pages.
    Provides CRUD operations for ContentPage model instances.
    Requires admin privileges.
    """
    queryset = ContentPage.objects.all().order_by('title')
    serializer_class = ContentPageSerializer
    permission_classes = [IsAdminUser]
