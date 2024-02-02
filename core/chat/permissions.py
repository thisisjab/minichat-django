from uuid import UUID

from django.contrib.auth import get_user_model

from core.chat import models

User = get_user_model()


def __check_chat_exists(chat_id: UUID):
    chat = models.Chat.objects.filter(id=chat_id)
    if not chat.exists():
        return False

    return True


def check_user_is_a_participant(user: User, chat_id: UUID):
    """Check if chat exists and user is a participant of it."""

    if not __check_chat_exists(chat_id):
        return False

    if not user.participations.filter(chat__id=chat_id, is_active=True).exists():
        return False

    return True
