from django.contrib.auth.backends import BaseBackend
from accounts.models import CustomUser


class CustomAuthBackend(BaseBackend):
    """
    Backend d'authentification personnalisée pour utiliser l'email et le mot de passe.
    """
    pass
