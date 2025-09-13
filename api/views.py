# api/views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny
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
