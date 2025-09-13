# api/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import User, Challenge, Solve
from .serializers import UserSerializer, ChallengeListSerializer, ChallengeDetailSerializer, FlagSubmissionSerializer


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


class SubmitFlagView(APIView):
    """
    API endpoint for submitting a flag for a challenge.
    Requires authentication.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FlagSubmissionSerializer # Used for request body validation

    def post(self, request, pk, *args, **kwargs):
        """
        Handles the submission of a flag for a specific challenge.
        """
        challenge = get_object_or_404(Challenge, pk=pk, is_published=True)
        user = request.user

        # 1. Check if the user has already solved this challenge
        if Solve.objects.filter(user=user, challenge=challenge).exists():
            return Response(
                {"detail": "Challenge already solved."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Validate the incoming flag data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        submitted_flag = serializer.validated_data['flag']

        # 3. Compare the submitted flag with the challenge's flag (case-insensitive and strip whitespace)
        if submitted_flag.strip().lower() == challenge.flag.strip().lower():
            # Flag is correct
            with transaction.atomic():
                # Create a Solve record
                Solve.objects.create(
                    user=user,
                    challenge=challenge,
                    points_awarded=challenge.points # For static scoring initially
                )

                # Update user's score
                user.score += challenge.points
                user.save()

                # Check for first blood if not already set
                if not challenge.first_blood:
                    challenge.first_blood = user
                    challenge.save()

            return Response(
                {"detail": "Flag submitted successfully!", "points_awarded": challenge.points},
                status=status.HTTP_200_OK
            )
        else:
            # Flag is incorrect
            return Response(
                {"detail": "Incorrect flag."},
                status=status.HTTP_400_BAD_REQUEST
            )
