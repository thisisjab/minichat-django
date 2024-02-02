import uuid
from typing import Self

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils.models import TimeStampedModel

User = get_user_model()


class Participation(models.Model):
    """Model that represents a many-to-many relation between a chat and user."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="participations",
        verbose_name=_("User"),
    )
    chat = models.ForeignKey(
        "Chat",
        on_delete=models.CASCADE,
        related_name="participations",
    )
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name=_("Is active"),
    )


class Chat(models.Model):
    """Model that represents a chat between two or more users.

    Raises:
        ValidationError: Validation error raised more that two users are added as participants.
    """

    class Type(models.TextChoices):
        PRIVATE = "P", _("Private Chat")
        GROUP = "G", _("Group Chat")

    id = models.UUIDField(
        primary_key=True,
        blank=False,
        null=False,
        default=uuid.uuid4(),
        verbose_name=_("ID"),
    )

    participants = models.ManyToManyField(
        User,
        related_name="chats",
        through=Participation,
        verbose_name=_("Participants"),
    )

    type = models.CharField(
        max_length=1,
        choices=Type.choices,
        blank=False,
        null=False,
    )

    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
    )

    def clean(self: Self) -> None:
        # In private conversations only two users can participate at most
        if self.type == self.Type.PRIVATE and self.participants.count() > 2:
            raise ValidationError(_("Only two users can be added to one private chat."))

        return super().clean()

    def __str__(self: Self) -> str:
        # TODO: complete this function
        return super().__str__()


class BaseMessage(TimeStampedModel):
    """Base model for any message sent in a chat."""

    id = models.UUIDField(
        primary_key=True,
        blank=False,
        null=False,
        default=uuid.uuid4(),
        verbose_name=_("ID"),
    )

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_("Chat"),
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="sent_messages",
        verbose_name=_("Sender"),
    )

    class Meta:
        abstract = True


class TextMessage(BaseMessage):
    body = models.CharField(max_length=255, verbose_name=_("Body"))
