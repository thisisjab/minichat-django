from typing import Any, Self

from django.forms import ModelForm, ValidationError

from core.chat import models


class PrivateChatAddForm(ModelForm):
    class Meta:
        model = models.PrivateChat
        fields = ["participants"]

    def clean(self: Self) -> dict[str, Any]:
        participants = self.cleaned_data.get("participants", None)

        if participants and participants.count() != 2:
            raise ValidationError("A private chat must have 2 and only 2 participants.")

        existing_private_chat = models.PrivateChat.objects.filter(
            participants=participants[0]
        )

        for participant in participants[1:]:
            existing_private_chat = existing_private_chat.filter(
                participants=participant
            )

        if existing_private_chat.exists():
            raise ValidationError("Another private chat exists for selected users.")

        return super().clean()
