# api/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Sum, Max, Count
from django.db.models.functions import Coalesce # Import Coalesce for handling NULLs
from rest_framework.exceptions import ValidationError

from .models import User, Challenge, Solve, Hint, UnlockedHint, Team, CTFSetting
from .serializers import (
    UserSerializer,
    ChallengeListSerializer,
    ChallengeDetailSerializer,
    FlagSubmissionSerializer,
    HintSerializer,
    TeamListSerializer,
    TeamDetailSerializer,
    TeamCreateSerializer,
    LeaderboardSerializer,
)


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

    def get_serializer_context(self):
        """
        Passes the request context to the serializer,
        which is needed by the HintSerializer to determine if a hint is unlocked.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


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
        Implements dynamic scoring logic based on CTFSetting.
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
                ctf_settings = CTFSetting.load()
                points_awarded_for_this_solve = challenge.points # Default to current points

                if ctf_settings.scoring_mode == 'dynamic' and challenge.is_dynamic:
                    # Calculate current number of solves for this challenge *before* this solve
                    current_solves_count = Solve.objects.filter(challenge=challenge).count()

                    # Apply dynamic scoring formula: points decay linearly per solve
                    # points = max(minimum_points, initial_points - (num_solves * decay_factor))
                    calculated_points = max(
                        challenge.minimum_points,
                        challenge.initial_points - (current_solves_count * challenge.decay_factor)
                    )
                    
                    points_awarded_for_this_solve = calculated_points # Points for the current solver

                    # Update the challenge's current points for *future* solves
                    challenge.points = calculated_points
                    challenge.save()
                
                # Create a Solve record with the points awarded to THIS user
                Solve.objects.create(
                    user=user,
                    challenge=challenge,
                    points_awarded=points_awarded_for_this_solve
                )

                # Update user's score
                user.score += points_awarded_for_this_solve
                user.save()

                # Check for first blood if not already set
                if not challenge.first_blood:
                    challenge.first_blood = user
                    challenge.save()

            return Response(
                {"detail": "Flag submitted successfully!", "points_awarded": points_awarded_for_this_solve},
                status=status.HTTP_200_OK
            )
        else:
            # Flag is incorrect
            return Response(
                {"detail": "Incorrect flag."},
                status=status.HTTP_400_BAD_REQUEST
            )


class UnlockHintView(APIView):
    """
    API endpoint for users to unlock a hint for a challenge.
    Requires authentication.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, *args, **kwargs):
        """
        Allows an authenticated user to unlock a specific hint.
        Deducts cost from user's score and creates an UnlockedHint record.
        """
        hint = get_object_or_404(Hint, pk=pk)
        user = request.user

        # Check if the user has already unlocked this hint
        if UnlockedHint.objects.filter(user=user, hint=hint).exists():
            return Response(
                {"detail": "You have already unlocked this hint."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the user has enough score to unlock the hint
        if user.score < hint.cost:
            return Response(
                {"detail": f"Insufficient score. You need {hint.cost} points to unlock this hint."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # Deduct points from user's score
            user.score -= hint.cost
            user.save()

            # Create an UnlockedHint record
            UnlockedHint.objects.create(user=user, hint=hint)

        return Response(
            {"detail": "Hint unlocked successfully!", "cost_deducted": hint.cost},
            status=status.HTTP_200_OK
        )


class TeamListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing teams and creating a new team.
    Authenticated users can list all teams.
    Authenticated users not in a team can create a new team and automatically join it.
    """
    queryset = Team.objects.all().order_by('name')
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TeamCreateSerializer
        return TeamListSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.team:
            raise ValidationError({"detail": "You are already part of a team. Please leave your current team to create a new one."})
        
        with transaction.atomic():
            team = serializer.save()
            user.team = team
            user.save()


class TeamDetailView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a single team's details, including its members.
    Requires authentication.
    """
    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer
    permission_classes = (IsAuthenticated,)


class JoinTeamView(APIView):
    """
    API endpoint for an authenticated user to join a specific team.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        team = get_object_or_404(Team, pk=pk)

        if user.team:
            return Response(
                {"detail": f"You are already part of a team: {user.team.name}. Please leave your current team to join another."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            user.team = team
            user.save()

        return Response(
            {"detail": f"Successfully joined team '{team.name}'."},
            status=status.HTTP_200_OK
        )


class LeaveTeamView(APIView):
    """
    API endpoint for an authenticated user to leave their current team.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user

        if not user.team:
            return Response(
                {"detail": "You are not currently part of any team."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        team_name = user.team.name
        with transaction.atomic():
            user.team = None
            user.save()

        return Response(
            {"detail": f"Successfully left team '{team_name}'."},
            status=status.HTTP_200_OK
        )


class LeaderboardView(generics.ListAPIView):
    """
    API endpoint for displaying the competition leaderboard.
    Shows teams ordered by total score and last solve time.
    Requires authentication.
    """
    serializer_class = LeaderboardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Constructs a queryset for the leaderboard, annotating teams with
        their total score and the timestamp of their last solve.
        """
        queryset = Team.objects.annotate(
            # Calculate total score for each team by summing scores of all its members.
            # Coalesce handles cases where a team has no members or members have no score, defaulting to 0.
            total_score=Coalesce(Sum('members__score'), 0, output_field=models.IntegerField()),
            # Find the latest solve time among all members of the team.
            # Coalesce handles teams with no solves by defaulting to NULL.
            last_solve_time=Coalesce(Max('members__solves__solved_at'), None, output_field=models.DateTimeField())
        ).order_by('-total_score', 'last_solve_time') # Order by score (desc) then by solve time (asc for tie-break)
        
        return queryset
