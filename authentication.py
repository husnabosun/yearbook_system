from django.contrib.auth.backends import BaseBackend
import re
from django.contrib.auth import get_user_model


class MyBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            return None
        if re.match(r'^\+?\d{1,10}$', username):
            try:
                user = UserModel.objects.get(student_number=username)
                if user.check_password(password):
                    return user
            except UserModel.DoesNotExist:
                return None
        else:
            try:
                user = UserModel.objects.get(username=username)
                if user.check_password(password):
                    return user
            except UserModel.DoesNotExist:
                return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
