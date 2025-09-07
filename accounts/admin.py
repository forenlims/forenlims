# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin view for CustomUser model."""

    # Fields to display in the list view
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_superuser',
        'is_active',
        'date_joined',
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    # Fields to edit in the admin form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        (
            'Permissions',
            {
                'fields': (
                    'is_staff',
                    'is_superuser',
                    'is_active',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to use when adding a new user via admin
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'is_staff',
                    'is_superuser',
                    'is_active',
                ),
            },
        ),
    )

    # Fields to search by
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

# Register your models here.

# Register your models here.
