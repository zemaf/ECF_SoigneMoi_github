from rest_framework.permissions import BasePermission

from accounts.models import CustomUser
from soignemoiwebsite.models import Medecin


class IsMedecin(BasePermission):
    """
    Permission qui autorise uniquement les médecins.
    """
    def has_permission(self, request, view):
        # vérifie si l'utilisateur est authentifié et s'il est un médecin
        user = Medecin.objects.get(pk=request.user.pk)
        print(f"voici le mail {user.email}, user est authentifié: {user.is_authenticated}, et user a un matricule : {hasattr(user, 'matricule_medecin')}")
        return user.is_authenticated and hasattr(user, 'matricule_medecin')
