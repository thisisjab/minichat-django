from typing import Any, Self

from django.forms import ModelForm, ValidationError

from core.chat import models, utils


class PrivateChatAddForm(ModelForm):
    class Meta:
        model = models.PrivateChat
        fields = ["participants"]

    def clean(self: Self) -> dict[str, Any]:
        participants = self.cleaned_data.get("participants", None)

        if participants and participants.count() != 2:
            raise ValidationError("A private chat must have 2 and only 2 participants.")

        if utils.check_if_chat_exists_for_participants(participants):
            raise ValidationError("Another private chat exists for selected users.")

        return super().clean()
