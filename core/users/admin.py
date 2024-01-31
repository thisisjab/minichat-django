from typing import Self

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from core.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for `User` model."""

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                ),
            },
        ),
    )
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "id",
                    "username",
                    "email",
                    "password",
                ],
            },
        ),
        (
            _("Personal info"),
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "gender",
                    "birth_date",
                ],
            },
        ),
        (
            _("Permissions"),
            {
                "fields": [
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "is_deleted",
                    "email_verified",
                    "groups",
                    "user_permissions",
                ],
            },
        ),
        (
            _("Important dates"),
            {
                "fields": [
                    "last_login",
                    "created_at",
                    "modified_at",
                ],
            },
        ),
    ]
    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "is_verified",
        "is_active",
    ]
    readonly_fields = [
        "id",
        "last_login",
        "modified_at",
        "created_at",
    ]
    list_filter = [
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
        "is_verified",
        "is_deleted",
        "email_verified",
        "gender",
    ]
    search_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
    ]
    ordering = [
        "username",
    ]
    filter_horizontal = [
        "groups",
        "user_permissions",
    ]
    actions = [
        "activate_users",
        "deactivate_users",
    ]

    @admin.action(description="Make selected users activated.")
    def activate_users(
        modeladmin: Self, request: HttpRequest, queryset: QuerySet
    ) -> None:
        updated = queryset.update(is_active=True)
        modeladmin.message_user(
            request,
            ngettext(
                "%d user was successfully marked as activated.",
                "%d users were successfully marked as activated.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(description="Make selected users deactivated.")
    def deactivate_users(
        modeladmin: Self, request: HttpRequest, queryset: QuerySet
    ) -> None:
        updated = queryset.update(is_active=False)
        modeladmin.message_user(
            request,
            ngettext(
                "%d user was successfully marked as deactivated.",
                "%d users were successfully marked as deactivated.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )
