# api/urls.py
from django.urls import path
from .views import RegisterView, ProfileView, ChallengeListView, ChallengeDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('challenges/', ChallengeListView.as_view(), name='challenge_list'),
    path('challenges/<int:pk>/', ChallengeDetailView.as_view(), name='challenge_detail'),
    # Other API paths will be added here
]
