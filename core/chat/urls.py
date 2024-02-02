from django.urls import path

from core.chat import views

app_name = "chat"

urlpatterns = [
    path("", views.ChatListView.as_view(), name="list"),
    path("<uuid:id>/", views.ConversationView.as_view(), name="conversation"),
]
