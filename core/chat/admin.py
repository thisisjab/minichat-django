from django.contrib import admin

from core.chat import models

# TODO: complete model admins


@admin.register(models.Participation)
class ParticipationAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    ...


@admin.register(models.TextMessage)
class TextMessageAdmin(admin.ModelAdmin):
    ...
