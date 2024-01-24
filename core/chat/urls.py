from django.urls import path

from core.chat import views

app_name = "chat"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("<str:room_name>/", views.RoomView.as_view(), name="room"),
]
