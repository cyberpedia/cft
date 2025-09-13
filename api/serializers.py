# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Team, Tag, Challenge, Solve


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.
    Configured for both user registration (create) and profile management (retrieve/update).
    - 'password' is write-only and handled securely.
    - 'username' is writable on creation but read-only for updates.
    - 'email', 'first_name', 'last_name' are updatable.
    - 'score' and 'team_name' are read-only.
    """
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})
    team_name = serializers.CharField(source='team.name', read_only=True, allow_null=True, help_text="The name of the user's team.")

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'score', 'team_name')
        read_only_fields = ('score', 'team_name',) # score and team_name are never directly editable
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}, # Password is not required for profile updates
            # 'username' is writable on create, and read-only for updates handled in the update method.
        }

    def create(self, validated_data):
        """
        Create and return a new `User` instance, with the password hashed.
        Ensures essential fields like username, email, and password are provided for registration.
        """
        # Enforce password requirement for creation
        if not validated_data.get('password'):
            raise serializers.ValidationError({"password": "This field is required for registration."})
        
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance.
        - Prevents updating the 'username' field after creation.
        - Handles password hashing if the password is included in the update.
        """
        # Prevent username from being updated after creation
        if 'username' in validated_data:
            # We explicitly raise an error to indicate that username is not modifiable.
            raise serializers.ValidationError({"username": "Username cannot be updated after creation."})

        # Handle password update separately to ensure it's hashed
        if 'password' in validated_data:
            instance.password = make_password(validated_data.pop('password'))
            
        # Update other allowed fields (email, first_name, last_name)
        return super().update(instance, validated_data)


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tag model.
    """
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ChallengeListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing challenges.
    Includes id, name, points, and tags.
    """
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Challenge
        fields = ('id', 'name', 'points', 'tags')


class ChallengeDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving a single challenge's details.
    Includes id, name, points, description, and tags.
    Crucially, the 'flag' field is explicitly excluded.
    """
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Challenge
        fields = ('id', 'name', 'points', 'description', 'tags')
        # Explicitly exclude the 'flag' field for security reasons
        read_only_fields = ('id', 'name', 'points', 'description', 'tags', 'is_published', 'is_dynamic', 'created_at', 'updated_at', 'first_blood')
        # If you were to use 'exclude', it would look like:
        # exclude = ('flag',)
        # But 'fields' is preferred for clarity and security when excluding critical data.
