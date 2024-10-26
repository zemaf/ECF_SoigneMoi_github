import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from accounts.models import CustomUser
from soignemoiwebsite.models import Avis, Patient, Medecin, Administrateur, Medicament, Prescription, Sejour, Specialite


# def test_verbose_name_plural():
#     """
#     Tester que le nom au pluriel de l'avis est correctement défini
#     """
#     assert str(Avis._meta.verbose_name_plural) == "Avis"

# ---Fixtures---
# on va utiliser les fixtures pour réutiliser le code dans nos différents tests, on évite les répétitions de code


@pytest.fixture
def custom_user(db):
    return CustomUser.objects.create(
        email="user@example.com",
        password="alimahfoud",
        nom="Dupont",
        prenom="Jean",
        adresse="123 Rue Exemple",
        genre="M",
        is_active=True
    )


@pytest.fixture
def specialite(db):
    return Specialite.objects.create(nom="Cardiologie")


@pytest.fixture
def medecin(db, specialite):
    return Medecin.objects.create(
        email="medecin@example.com",
        genre="Mme",
        nom="Martin",
        prenom="Marie",
        matricule_medecin="M12345",
        specialite=specialite
    )


@pytest.fixture
def patient(db):
    return Patient.objects.create(
        email="patient@example.com",
        nom="Doe",
        prenom="John",
        adresse="456 Rue Santé",
        genre="M"
    )

# --- Tests ---


def test_custom_user_validators(custom_user):
    """
    Teste les RegexValidator pour les champs nom, prenom et adresse.
    """
    # Test nom et prénom validés
    assert custom_user.nom == "Dupont"
    assert custom_user.prenom == "Jean"

    # Test adresse validée
    custom_user.adresse = "456 Rue de l'Exemple"
    custom_user.full_clean()  # Appelle les validateurs de champ

    # Test adresse invalide
    custom_user.adresse = "Adresse invalide @@@"
    with pytest.raises(ValidationError):
        custom_user.full_clean()


def test_specialite_unique(specialite):
    """
    Teste que le nom de la spécialité est unique.
    """
    with pytest.raises(IntegrityError):
        Specialite.objects.create(nom="Cardiologie")


def test_medecin_string_representation(medecin):
    """
    Teste la représentation en chaîne de caractères du modèle Medecin.
    """
    assert str(medecin) == f"Dr {medecin.nom} {medecin.prenom}, spécialité : {medecin.specialite}"


def test_prescription_dates(patient, medecin):
    """
    Teste la création d'une prescription avec des dates valides et invalides.
    """
    prescription = Prescription(
        user=patient,
        medecin=medecin,
        date_debut_traitement=timezone.now().date(),
        date_fin_traitement=timezone.now().date() - timezone.timedelta(days=1)
    )
    with pytest.raises(ValidationError):
        prescription.full_clean()  # Test si la date de fin est antérieure à la date de début


def test_avis_plural_verbose_name():
    """
    Teste le nom pluriel du modèle Avis.
    """
    assert str(Avis._meta.verbose_name_plural) == "Avis"


def test_sejour_clean_method(patient, medecin, specialite):
    """
    Teste la méthode clean() du modèle Sejour pour valider les dates d'entrée et de sortie.
    """
    sejour = Sejour(
        date_entree=timezone.now().date(),
        date_sortie=timezone.now().date() - timezone.timedelta(days=1),
        motif="Check-up complet",
        user=patient,
        specialite=specialite,
        medecin=medecin
    )
    with pytest.raises(ValidationError) as e:
        sejour.clean()
    assert "La date de sortie doit être postérieure à l'entrée!" in str(e.value)


def test_avis_multiples_meme_patient(patient, medecin):
    """
    Teste si on peut avoir plusieurs avis pour le même patient
    """
    avis1 = Avis.objects.create(
        user=patient,
        medecin=medecin,
        libelle="Première consultation",
        date=timezone.now().date(),
        description="Très bon médecin."
    )

    avis2 = Avis.objects.create(
            user=patient,
            medecin=medecin,
            libelle="Deuxième consultation",
            date=timezone.now().date(),
            description="Consultation de suivi."
        )

    assert Avis.objects.count() == 2
