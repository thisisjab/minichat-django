from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from core.users.models import User


class UsernameOrEmailModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        try:
            user_model = User
            user = user_model.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except user_model.DoesNotExist:
            user_model().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
