# api/views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import UserSerializer


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
