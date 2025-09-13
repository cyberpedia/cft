# api/urls.py
from django.urls import path
from .views import (
    RegisterView,
    ProfileView,
    ChallengeListView,
    ChallengeDetailView,
    SubmitFlagView,
    UnlockHintView,
    TeamListCreateView,
    TeamDetailView,
    JoinTeamView,
    LeaveTeamView,
    LeaderboardView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('challenges/', ChallengeListView.as_view(), name='challenge_list'),
    path('challenges/<int:pk>/', ChallengeDetailView.as_view(), name='challenge_detail'),
    path('challenges/<int:pk>/submit/', SubmitFlagView.as_view(), name='submit_flag'),

    path('hints/<int:pk>/unlock/', UnlockHintView.as_view(), name='unlock_hint'),

    path('teams/', TeamListCreateView.as_view(), name='team_list_create'),
    path('teams/<int:pk>/', TeamDetailView.as_view(), name='team_detail'),
    path('teams/<int:pk>/join/', JoinTeamView.as_view(), name='team_join'),
    path('teams/leave/', LeaveTeamView.as_view(), name='team_leave'),
    
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    # Other API paths will be added here
]
