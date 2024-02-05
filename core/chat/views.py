from typing import Any, Self

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.chat.utils import get_last_messages_for_user


class ChatListView(LoginRequiredMixin, TemplateView):
    template_name = "chat/list.html"

    def get_context_data(self: Self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        user = self.request.user

        last_messages = get_last_messages_for_user(user)

        context["last_messages"] = last_messages
        return context
