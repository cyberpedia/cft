# api/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Team, Tag, Challenge, Solve


# Register Team model
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


# Register User model
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Fields to display in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'score', 'team')
    # Fields to make searchable
    search_fields = ('username', 'email', 'team__name')
    # Fields to filter by
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'team')
    # Fields to edit on the detail page
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('score', 'team')}),
    )
    # Fields to add when creating a new user in the admin
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('score', 'team')}),
    )


# Register Tag model
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


# Register Challenge model
@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'points', 'is_published', 'is_dynamic', 'first_blood', 'created_at', 'updated_at')
    list_filter = ('is_published', 'is_dynamic', 'tags')
    search_fields = ('name', 'description', 'flag')
    # Automatically populate the many-to-many field for tags
    filter_horizontal = ('tags',)


# Register Solve model
@admin.register(Solve)
class SolveAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'solved_at', 'points_awarded')
    list_filter = ('solved_at', 'challenge', 'user')
    search_fields = ('user__username', 'challenge__name')
    readonly_fields = ('solved_at', 'points_awarded') # Typically solved_at and points_awarded are set programmatically
