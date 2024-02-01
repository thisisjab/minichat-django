from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.users.forms import UserCreationForm
from core.users.models import User


class SignUpView(CreateView):
    form_class = UserCreationForm
    model = User
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
