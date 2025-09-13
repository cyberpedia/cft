# api/views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Challenge
from .serializers import UserSerializer, ChallengeListSerializer, ChallengeDetailSerializer


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    Allows creation of new User instances without requiring authentication.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,) # Anyone can register


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for viewing and updating the authenticated user's profile.
    Users can only access and modify their own profile data.
    """
    queryset = User.objects.all() # Required, but get_object will override it.
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,) # Only authenticated users can access this.

    def get_object(self):
        """
        Returns the user instance associated with the current request.
        This ensures users can only view and update their own profiles.
        """
        return self.request.user


class ChallengeListView(generics.ListAPIView):
    """
    API endpoint for listing all published challenges.
    Only includes challenges where is_published is True.
    Requires authentication.
    """
    queryset = Challenge.objects.filter(is_published=True).order_by('points', 'name')
    serializer_class = ChallengeListSerializer
    permission_classes = (IsAuthenticated,)


class ChallengeDetailView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a single published challenge's details.
    Only allows access to challenges where is_published is True.
    Requires authentication.
    """
    queryset = Challenge.objects.filter(is_published=True)
    serializer_class = ChallengeDetailSerializer
    permission_classes = (IsAuthenticated,)
