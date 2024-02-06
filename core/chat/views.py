from typing import Any, Self

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from core.chat import models
from core.chat.utils import (
    check_if_chat_exists_for_participants,
    get_last_messages_for_user,
)

User = get_user_model()


class ChatListView(LoginRequiredMixin, TemplateView):
    template_name = "chat/list.html"

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        user = self.request.user

        last_messages = get_last_messages_for_user(user)

        context["last_messages"] = last_messages
        return context


class ConversationView(LoginRequiredMixin, TemplateView):
    template_name = "chat/conversation.html"

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        user = self.request.user
        peer_user = get_object_or_404(User, username=kwargs.get("username", None))
        last_messages = get_last_messages_for_user(user)

        context = super().get_context_data(**kwargs)
        context["peer_user"] = peer_user
        context["last_messages"] = last_messages

        if not check_if_chat_exists_for_participants([user, peer_user]):
            private_chat = models.PrivateChat.objects.create()
            private_chat.participants.add(user)
            private_chat.participants.add(peer_user)
            context["chat_id"] = private_chat.id
            context["chat_messages"] = list()
            return context

        chat = (
            models.PrivateChat.objects.filter(participants=user)
            .filter(participants=peer_user)
            .first()
        )

        context["chat_id"] = chat.id
        context["chat_messages"] = chat.messages.order_by("modified_at").all()

        return context
