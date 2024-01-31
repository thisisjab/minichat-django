import uuid
from typing import Self

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.users.managers import UserManager
from core.utils.models import TimeStampedModel


class UsernameValidator(RegexValidator):
    regex = r"^(?=.{4,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"


class User(AbstractBaseUser, TimeStampedModel, PermissionsMixin):
    """User model representing a user in the application."""

    class Gender(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")
        OTHER = "O", _("Other")

    username_validator = UsernameValidator()

    id = models.UUIDField(
        _("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        serialize=False,
    )

    username = models.CharField(
        _("Username"),
        unique=True,
        validators=[username_validator],
    )

    first_name = models.CharField(
        _("First Name"),
        null=False,
        blank=False,
    )

    last_name = models.CharField(_("Last Name"), null=False, blank=False)

    birth_date = models.DateField(
        _("Birth date"),
        null=True,
        blank=True,
    )

    gender = models.CharField(
        _("Gender"),
        max_length=1,
        choices=Gender.choices,
        default=Gender.MALE,
    )

    email = models.EmailField(_("Email"), unique=True, null=False, blank=False)
    email_verified = models.BooleanField(_("Email is verified"), default=False)

    is_staff = models.BooleanField(_("Is staff"), default=False)
    is_active = models.BooleanField(_("Is active"), default=True)
    is_verified = models.BooleanField(_("Is verified"), default=False)
    is_deleted = models.BooleanField(_("Is deleted"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        indexes = [
            models.Index(fields=["username", "created_at"]),
        ]
        ordering = ["-created_at"]
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def is_member_of_group(self: Self, group: str):
        """Check if the user is a member of the specified group.

        Args:
            group (str): The name of the group to check.

        Returns:
            bool: True if the user is a member of the group, False otherwise.
        """
        return self.groups.filter(name=group).exists()

    def __str__(self: Self) -> str:
        return self.username
