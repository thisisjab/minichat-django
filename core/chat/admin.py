from typing import Self

from django.contrib import admin
from django.template.defaultfilters import truncatechars
from django.urls import reverse
from django.utils.html import format_html

from core.chat import models


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
        "receiver",
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

    @admin.display(ordering="receiver__username")
    def receiver_username(self: Self, message: models.PrivateTextMessage):
        link = reverse(
            "admin:users_user_change",
            args=[message.receiver.pk],
        )
        return format_html(
            '<a href="{}">{}</a>',
            link,
            message.receiver.username,
        )
