import uuid
from typing import Self

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.translation import gettext_lazy as _

from core.utils.models import TimeStampedModel

User = get_user_model()


class PrivateChat(models.Model):
    """This model represents a private chat between two individuals.

    NOTE: As m2m fields cannot be validated in model level, always use forms or
    serializers to validate that 2 and only 2 participants exist. Also, before
    creating new chat instance make sure that chat instance does not exist.
    """

    id = models.UUIDField(
        _("Id"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        null=False,
        blank=False,
    )

    participants = models.ManyToManyField(
        User,
        related_name="private_chats",
        verbose_name=_("Participants"),
    )

    class Meta:
        verbose_name = "private chat"
        verbose_name_plural = "private chats"

    def __str__(self: Self) -> str:
        # NOTE: remember to pre_fetch `participants` field
        return ", ".join(
            [user.username for user in self.participants.order_by("username").all()]
        )


class BasePrivateMessage(TimeStampedModel):
    """Base class for all type of private messages (text, image, etc.)"""

    id = models.UUIDField(
        _("Id"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        null=False,
        blank=False,
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="sent_private_messages",
        blank=False,
        null=False,
        verbose_name=_("Sender"),
    )

    related_chat = models.ForeignKey(
        PrivateChat,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_("Related chat"),
    )

    class Meta:
        abstract = True

    def clean(self: Self) -> None:
        if self.sender not in self.related_chat.participants.all():
            raise ValidationError(
                "Cannot send a message since sender is not "
                "a participant of the related chat."
            )

        return super().clean()


class PrivateTextMessage(BasePrivateMessage):
    """This class represents a basic text message sent in a private chat."""

    body = models.TextField(
        null=False,
        blank=False,
        validators=[MaxLengthValidator(4096)],
        verbose_name=_("Body"),
    )

    class Meta:
        verbose_name = "Private text message"
        verbose_name_plural = "Private text messages"

    def __str__(self: Self):
        return truncatechars(self.body, 50)
