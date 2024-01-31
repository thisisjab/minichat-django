# Generated by Django 5.0.1 on 2024-01-31 09:35

import uuid

from django.db import migrations, models

import core.users.managers
import core.users.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text=(
                            "Designates that this user has all "
                            "permissions without explicitly assigning them."
                        ),
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(auto_now=True, verbose_name="Modified at"),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        unique=True,
                        validators=[core.users.models.UsernameValidator()],
                        verbose_name="Username",
                    ),
                ),
                ("first_name", models.CharField(verbose_name="First Name")),
                ("last_name", models.CharField(verbose_name="Last Name")),
                (
                    "birth_date",
                    models.DateField(blank=True, null=True, verbose_name="Birth date"),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
                        default="M",
                        max_length=1,
                        verbose_name="Gender",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Email"
                    ),
                ),
                (
                    "email_verified",
                    models.BooleanField(
                        default=False, verbose_name="Email is verified"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(default=False, verbose_name="Is staff"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is active"),
                ),
                (
                    "is_verified",
                    models.BooleanField(default=False, verbose_name="Is verified"),
                ),
                (
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="Is deleted"),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text=(
                            "The groups this user belongs to. A user will "
                            "get all permissions granted to each of their groups."
                        ),
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(
                        fields=["username", "created_at"],
                        name="users_user_usernam_3f2989_idx",
                    )
                ],
            },
            managers=[
                ("objects", core.users.managers.UserManager()),
            ],
        ),
    ]
