from typing import Self
from uuid import UUID

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from core.chat import models
from core.chat.permissions import check_user_is_a_participant

User = get_user_model()


class ChatListView(LoginRequiredMixin, View):
    def get(self: Self, request: HttpRequest):
        user_active_participations = models.Participation.objects.filter(
            user=request.user, is_active=True
        ).all()

        user_active_chats = []

        for participation in user_active_participations:
            chat_name = (
                participation.chat.participations.exclude(user=request.user)
                .last()
                .user.username
            )

            chat = {
                "id": participation.chat.id,
                "type": participation.chat.type,
                "last_modified_at": participation.chat.last_modified_at(),
                "name": chat_name,
            }

            user_active_chats.append(chat)

        return render(
            request, "chat/list.html", context={"user_active_chats": user_active_chats}
        )


class ConversationView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request: HttpRequest, id: UUID):
        user_active_participations = models.Participation.objects.filter(
            user=request.user, is_active=True
        ).all()

        user_active_chats = []

        for participation in user_active_participations:
            chat_name = (
                participation.chat.participations.exclude(user=request.user)
                .last()
                .user.username
            )

            chat = {
                "id": participation.chat.id,
                "type": participation.chat.type,
                "last_modified_at": participation.chat.last_modified_at(),
                "name": chat_name,
            }

            user_active_chats.append(chat)

        chat = (
            models.Chat.objects.prefetch_related("messages")
            .filter(id=self.kwargs["id"])
            .last()
        )

        chat_messages = []

        for message in chat.messages.all():
            chat_message = {
                "id": message.id,
                "body": message.body,
                "modified_at": message.modified_at,
                "is_sent": True if message.sender == request.user else False,
            }

            chat_messages.append(chat_message)

        return render(
            request,
            "chat/conversation.html",
            context={
                "chat_id": str(id),
                "user_active_chats": user_active_chats,
                "chat_messages": chat_messages,
            },
        )

    def test_func(self: Self):
        return check_user_is_a_participant(
            self.request.user,
            self.kwargs["id"],
        )
