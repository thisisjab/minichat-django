from typing import Any, Self

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from core.chat import models
from core.chat.utils import get_last_messages_for_user

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

        chat_messages = (
            models.PrivateTextMessage.objects.filter(
                Q(sender=user, receiver=peer_user) | Q(sender=peer_user, receiver=user)
            )
            .order_by("modified_at")
            .all()
        )

        context = super().get_context_data(**kwargs)

        last_messages = get_last_messages_for_user(user)

        context["last_messages"] = last_messages
        context["chat_messages"] = chat_messages

        return context
