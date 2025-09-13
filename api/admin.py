# api/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Team


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
