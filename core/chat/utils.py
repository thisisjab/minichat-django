from typing import List
from uuid import UUID

from django.contrib.auth import get_user_model

from core.chat import models

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
                        pk=user.pk
                    ).first(),
                }
            )

    return last_messages


def check_if_chat_exists_for_participants(participants: List[User]) -> bool:
    """Checks if a chat with given participants exists.

    Args:
        participants (List[User]): a list of `User` objects

    Returns:
        bool: True if there is a chat with given participants
    """
    existing_private_chat = models.PrivateChat.objects.filter(
        participants=participants[0]
    )

    for participant in participants[1:]:
        existing_private_chat = existing_private_chat.filter(participants=participant)

    if existing_private_chat.exists():
        return True

    return False


def check_user_is_a_participant_of_chat(user: UUID, chat_id: UUID) -> bool:
    """Check if given users is a participant of given chat (if exists).

    Args:
        user (User): User to check participation
        chat_id (UUID): Chat to check participation

    Returns:
        bool: True if chat exists and user is a participant of
    """

    return models.PrivateChat.objects.filter(pk=chat_id, participants=user).exists()


def get_or_create_private_chat(participants: List[User]):
    """Create a private chat for given users."""

    if check_if_chat_exists_for_participants(participants):
        return models.PrivateChat.objects.filter(participants__in=participants).first()
    else:
        private_chat = models.PrivateChat()
        private_chat.save()
        private_chat.participants.add(participants[0])
        private_chat.participants.add(participants[1])
        return private_chat


def create_user_channel_key(username: str):
    """Create a private group name for given username.

    Args:
        username (str): user's username to create group name
    """

    return f"user-{username}"
