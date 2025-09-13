# api/urls.py
from django.urls import path
from .views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # Other API paths will be added here
]
