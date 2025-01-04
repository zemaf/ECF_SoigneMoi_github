from rest_framework.permissions import BasePermission

from accounts.models import CustomUser
from soignemoiwebsite.models import Medecin


class IsMedecin(BasePermission):
    """
    Permission qui autorise uniquement les médecins.
    """
    def has_permission(self, request, view):  # view = instance de vue ou viewset dont l'accès est en cours d'évaluation
        # vérifie si l'utilisateur est authentifié et s'il est un médecin
        user = Medecin.objects.get(pk=request.user.pk)
        # print(f"voici le mail {user.email}, user est authentifié: {user.is_authenticated},
        # et user a un matricule : {hasattr(user, 'matricule_medecin')}")
        return user.is_authenticated and hasattr(user, 'matricule_medecin')


class IsSecretaire(BasePermission):
    """
    Permission permettant uniquement aux secrétaires d'accéder aux détails des patients pour une date donnée.
    """

    # def has_permission(self, request, view):
    #     # Vérifie si l'utilisateur est authentifié et s'il s'agit d'un.e secrétaire
    #     user = Secretaire.objects.get(pk=request.user.pk)
    #     return request.user.is_authenticated and hasattr(user, 'is_secretaire')
