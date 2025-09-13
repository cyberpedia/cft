# api/urls.py
from django.urls import path
from .views import RegisterView, ProfileView, ChallengeListView, ChallengeDetailView, SubmitFlagView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('challenges/', ChallengeListView.as_view(), name='challenge_list'),
    path('challenges/<int:pk>/', ChallengeDetailView.as_view(), name='challenge_detail'),
    path('challenges/<int:pk>/submit/', SubmitFlagView.as_view(), name='submit_flag'),
    # Other API paths will be added here
]
