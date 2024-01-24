from django.urls import path

from core.pages import views

app_name = "pages"

urlpatterns = [path("", views.IndexView.as_view(), name="index")]
