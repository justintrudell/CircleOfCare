from django.db import models
from django.contrib.auth.backends import ModelBackend
from circleofcare.models import CustomUser
import re

email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)


class BasicBackend:
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None


class EmailBackend(BasicBackend):
    def authenticate(self, email=None, password=None):
        if email_re.search(email):
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return None
        else:
            try:
                user = CustomUser.objects.get(username=email)
            except CustomUser.DoesNotExist:
                return None
        if user.check_password(password):
            return user
