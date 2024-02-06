from typing import Any, Self

from django.contrib import admin
from django.db.models import Count, F
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.template.defaultfilters import truncatechars
from django.urls import reverse
from django.utils.html import format_html

from core.chat import forms, models


@admin.register(models.PrivateChat)
class PrivateChatAdmin(admin.ModelAdmin):
    form = forms.PrivateChatAddForm
    list_display = ["id", "involved_users", "messages_count"]
    list_per_page = 20
    search_fields = ["participants"]
    search_help_text = "Search based on participants."

    def get_queryset(self: Self, request: HttpRequest) -> QuerySet[Any]:
        return (
            models.PrivateChat.objects.prefetch_related("participants")
            .annotate(messages_count=Count(F("messages")))
            .all()
        )

    def involved_users(self: Self, private_chat: models.PrivateChat):
        urls = []

        for user in private_chat.participants.all():
            url = reverse("admin:users_user_change", args=[user.pk])
            urls.append((url, user.username))

        return format_html(
            '<a href="{}">{}</a>, <a href="{}">{}</a>',
            *[item for url in urls for item in url],
        )

    @admin.display(ordering="messages_count")
    def messages_count(self: Self, private_chat: models.PrivateChat):
        return private_chat.messages_count

    def has_change_permission(self: Self, *args, **kwargs) -> bool:
        # Admin should not be able to change detail of a private chat (participants)
        return False


@admin.register(models.PrivateTextMessage)
class TextPrivateMessageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "message_body",
        "sender_username",
        "receiver_username",
        "modified_at",
        "created_at",
    ]

    list_filter = [
        "modified_at",
        "created_at",
    ]

    list_per_page = 20

    ordering = [
        "modified_at",
        "created_at",
    ]

    raw_id_fields = [
        "sender",
        # "receiver",
    ]

    readonly_fields = [
        "created_at",
        "modified_at",
    ]

    search_fields = [
        "body",
        "sender",
        "receiver",
    ]

    search_help_text = "Search by message body and sender/receiver name."

    def message_body(self: Self, message: models.PrivateTextMessage):
        return truncatechars(message.body, 50)

    @admin.display(ordering="sender__username")
    def sender_username(self: Self, message: models.PrivateTextMessage):
        link = reverse(
            "admin:users_user_change",
            args=[message.sender.pk],
        )
        return format_html(
            '<a href="{}">{}</a>',
            link,
            message.sender.username,
        )

    # @admin.display(ordering="receiver__username")
    def receiver_username(self: Self, message: models.PrivateTextMessage):
        receiver = message.related_chat.participants.exclude(
            pk=message.sender.pk
        ).first()
        link = reverse(
            "admin:users_user_change",
            args=[receiver.pk],
        )
        return format_html(
            '<a href="{}">{}</a>',
            link,
            receiver.username,
        )
