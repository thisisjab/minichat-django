from django.contrib.auth import get_user_model
from django.db.models import Q

from core.chat import models

User = get_user_model()


def get_last_messages_for_user(user: User):
    """Get last message of all conversations that a user is involved."""
    messages_related_to_user = (
        models.PrivateTextMessage.objects.filter(Q(sender=user) | Q(receiver=user))
        .order_by(
            "sender__id",
            "receiver__id",
            "-modified_at",
        )
        .distinct(
            "sender__id",
            "receiver__id",
        )
    )

    # NOTE: I needed a fresh copy previous queryset to do ordering
    # Django does not allow for ordering
    # Also, I have no idea that how to get a fresh copy of a queryset
    # TODO: find a better solution
    messages_related_to_user = sorted(
        messages_related_to_user, key=lambda m: m.modified_at, reverse=True
    )

    # Manually distinguishing `sender__id` and `receiver__id` regardless of order
    last_messages = []
    checked_users = set()

    for message in messages_related_to_user:
        print(message.sender.username, message.body)
        if not (
            message.sender.username in checked_users
            and message.receiver.username in checked_users
        ):
            last_messages.append(
                {
                    "body": message.body,
                    "modified_at": message.modified_at,
                    "user": (
                        message.receiver.username
                        if message.sender == user
                        else message.sender.get_username
                    ),
                }
            )
            checked_users.add(message.sender.username)
            checked_users.add(message.receiver.username)

    return last_messages
