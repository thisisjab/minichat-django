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

    receiver = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="received_private_messages",
        blank=False,
        null=False,
        verbose_name=_("Receiver"),
    )

    class Meta:
        abstract = True

    def clean(self: Self) -> None:
        if self.sender == self.receiver:
            raise ValidationError(_("Sender and receiver cannot be the same."))

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
