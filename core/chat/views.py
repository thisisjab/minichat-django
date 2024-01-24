from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request):
        return render(request, "chat/home.html")


class RoomView(View):
    def get(self, request, room_name):
        return render(request, "chat/room.html", context={"room_name": room_name})