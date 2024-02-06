from django.contrib.auth import get_user_model

User = get_user_model()


def get_last_messages_for_user(user: User):
    """Get last message of all conversations that a user is involved."""
    last_messages = []

    for chat in user.private_chats.all():
        last_message = chat.messages.all().order_by("modified_at").last()
        if last_message:
            last_messages.append(
                {
                    "body": last_message.body,
                    "modified_at": last_message.modified_at,
                    "user": last_message.related_chat.participants.exclude(
                        pk=last_message.sender.pk
                    ).first(),
                }
            )

    return last_messages
