# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Team, Tag, Challenge, Hint, UnlockedHint, Solve


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


class HintSerializer(serializers.ModelSerializer):
    """
    Serializer for the Hint model, conditionally showing text based on unlock status.
    """
    is_unlocked = serializers.SerializerMethodField(help_text="True if the current user has unlocked this hint.")

    class Meta:
        model = Hint
        fields = ('id', 'cost', 'is_unlocked', 'text')
        read_only_fields = ('id', 'cost', 'is_unlocked',) # Text is conditionally shown

    def get_is_unlocked(self, obj):
        """
        Determines if the request user has unlocked this hint.
        Requires 'request' in the serializer context.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UnlockedHint.objects.filter(user=request.user, hint=obj).exists()
        return False

    def to_representation(self, instance):
        """
        Conditionally includes the 'text' field based on 'is_unlocked'.
        """
        representation = super().to_representation(instance)
        if not representation.get('is_unlocked'):
            representation.pop('text', None) # Remove text if not unlocked
        return representation


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
    Includes id, name, points, description, file URL, and tags.
    Crucially, the 'flag' field is explicitly excluded.
    """
    tags = TagSerializer(many=True, read_only=True)
    hints = HintSerializer(many=True, read_only=True) # Nested hints using the new serializer
    file = serializers.FileField(read_only=True, source='file.url', allow_null=True) # Get URL for the file

    class Meta:
        model = Challenge
        fields = ('id', 'name', 'points', 'description', 'file', 'tags', 'hints')
        # Explicitly exclude the 'flag' field for security reasons
        read_only_fields = ('id', 'name', 'points', 'description', 'file', 'tags', 'hints', 'is_published', 'is_dynamic', 'created_at', 'updated_at', 'first_blood')


class FlagSubmissionSerializer(serializers.Serializer):
    """
    Serializer for submitting a flag to a challenge.
    Contains a single field: 'flag'.
    """
    flag = serializers.CharField(max_length=255, required=True, help_text="The flag to submit for the challenge.")


class TeamMemberSerializer(serializers.ModelSerializer):
    """
    A simplified UserSerializer for displaying team members.
    Only shows essential public information.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'score')
        read_only_fields = fields


class TeamListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing teams.
    """
    class Meta:
        model = Team
        fields = ('id', 'name')


class TeamDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving a single team's details, including its members.
    """
    members = TeamMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'members', 'created_at')
        read_only_fields = ('id', 'name', 'members', 'created_at')


class TeamCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new team.
    Only requires the team name.
    """
    class Meta:
        model = Team
        fields = ('name',)
