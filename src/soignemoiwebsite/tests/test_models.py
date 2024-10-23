import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from soignemoiwebsite.models import Avis, Patient, Medecin


def test_verbose_name_plural():
    """
    Tester que le nom au pluriel de l'avis est correctement défini
    """
    assert str(Avis._meta.verbose_name_plural) == "Avis"


# on va utiliser les fixtures pour réutiliser le code dans nos différents tests, on évite les répétitions de code
@pytest.fixture
def patient_fixture(db):  # accès à la base de données uniquement ici, via l'argument "db"
    return Patient.objects.create(
        genre="Mr",
        nom="Roux",
        prenom="Paul",
        email="p_r@email.com")


# @pytest.mark.django_db  => autre possibilité si on n'utilise pas de fixture
def test_representation_str_patient(patient_fixture):
    """
    Tester la relation entre les modèles Patient, Medecin et Avis.
    """
    # patient = Patient.objects.create(
    #     genre="Mr",
    #     nom="Roux",
    #     prenom="Paul",
    #     email="p_r@email.com")

    assert str(patient_fixture) == f" {patient_fixture.genre} {patient_fixture.nom} {patient_fixture.prenom}"
