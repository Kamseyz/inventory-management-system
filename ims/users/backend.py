# backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using their email and password.
    Use this for any Django project with email-based authentication.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Handle None values
        if username is None or password is None:
            return None
            
        try:
           
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            
            UserModel().set_password(password)
            return None
        except MultipleObjectsReturned:
            return None

        # Check password and if user can authenticate
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None