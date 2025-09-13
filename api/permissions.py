# api/permissions.py
from rest_framework import permissions
from .models import Solve, Challenge


class CanSubmitWriteUp(permissions.BasePermission):
    """
    Custom permission to check if a user can submit a write-up for a challenge.
    A user can submit a write-up only if:
    1. They are authenticated.
    2. They have successfully solved the challenge.
    """

    def has_permission(self, request, view):
        # Allow GET requests for listing (if any, though this view is CreateAPIView)
        # or other safe methods if it were a different view type.
        # For CreateAPIView (POST), we need to check permissions.
        if request.method not in permissions.SAFE_METHODS:
            # Check if the user is authenticated
            if not request.user.is_authenticated:
                return False

            # For POST requests, the challenge ID will be in request.data
            challenge_id = request.data.get('challenge')
            if not challenge_id:
                # If challenge_id is missing from data, let serializer validation handle it
                return True # Defer to serializer for validation issues like missing fields

            try:
                challenge = Challenge.objects.get(pk=challenge_id)
            except Challenge.DoesNotExist:
                # Challenge doesn't exist, let serializer/view handle invalid challenge ID
                return True # Defer to serializer/view
            
            # Check if the user has solved this specific challenge
            return Solve.objects.filter(user=request.user, challenge=challenge).exists()
        
        return True # For safe methods, or if it's not a POST, we don't apply this specific check here.
