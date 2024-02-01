from django.urls import path

from core.users import views

app_name = "users"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
]
