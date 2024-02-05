from django.urls import path

from core.chat import views

app_name = "chat"

urlpatterns = [
    path("list/", views.ChatListView.as_view(), name="list"),
]
