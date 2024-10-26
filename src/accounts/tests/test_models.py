import pytest
from django.core.exceptions import ValidationError

from soignemoiwebsite.models import Patient


# @pytest.fixture
# def custom_user(db):
#     adresse_malicious = "1234'; DROP TABLE Addresses;--"
#     return Patient(
#         genre="M",
#         nom="<script>alert('Hacked!');</script>",
#         prenom="Jean",
#         adresse=adresse_malicious,
#         email="test@example.com"
#     )


# on peut utiliser une autre méthode que les fixtures avec mark.django_db
@pytest.mark.django_db
def test_adresse_regex():
    # Adresse malicieuse que l'on veut rejeter
    adresse_malicious = "1234'; DROP TABLE Addresses;--"

    # Crée une instance de l'utilisateur sans la sauvegarder
    custom_user = Patient(
        genre="M",
        nom="<script>alert('Hacked!');</script>",
        prenom="Jean",
        adresse=adresse_malicious,
        email="test@example.com"
    )

    # Vérifie que la validation échoue (pour l'adresse et le nom)
    with pytest.raises(ValidationError) as exc_info:
        # full_clean effectue une validation complète des champs et des regex!
        custom_user.full_clean()  # donc après cela une erreur doit déjà être levée → test passed

    # Vérifie que l'erreur est due à l'adresse et au nom
    # ici, on va aller chercher précisément où se situe l'erreur et vérifier que les messages renvoyés sont les bons
    assert "adresse" and "nom" in exc_info.value.message_dict
    assert exc_info.value.message_dict["adresse"] == [
        "Mauvais format d'adresse"]
    assert exc_info.value.message_dict["nom"] == ["Le prénom ne peut contenir que des lettres, "
                                                  "espaces, apostrophes ou des tirets."]