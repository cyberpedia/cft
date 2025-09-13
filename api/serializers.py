# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Team # Import Team if needed for user creation, though not explicitly requested here

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model, primarily for registration.
    Ensures password is write-only and hashed on creation.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'score', 'team')
        read_only_fields = ('score', 'team') # Score and team will be managed separately or after registration

    def create(self, validated_data):
        """
        Create and return a new `User` instance, with the password hashed.
        """
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, with password handling.
        """
        if 'password' in validated_data:
            instance.password = make_password(validated_data.pop('password'))
        return super().update(instance, validated_data)
