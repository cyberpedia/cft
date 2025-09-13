# api/admin_views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import User, Team
from .serializers import AdminUserSerializer, AdminTeamSerializer


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
