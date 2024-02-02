from typing import Self

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from core.chat import models

User = get_user_model()


class HomeView(LoginRequiredMixin, View):
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
            request, "chat/home.html", context={"user_active_chats": user_active_chats}
        )


class RoomView(View):
    def get(self, request, room_name):
        return render(request, "chat/room.html", context={"room_name": room_name})
