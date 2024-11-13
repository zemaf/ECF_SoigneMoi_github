import pytest
from django.urls import reverse
from django.test import Client
from concurrent.futures import ThreadPoolExecutor
from soignemoiwebsite.models import Medecin, Sejour, Specialite, Patient
from datetime import date, timedelta, time


@pytest.mark.django_db
def test_concurrent_sejour_creation():
    client = Client()

    # Créer une spécialité et un médecin pour le test
    specialite = Specialite.objects.create(nom="zboubi")
    medecin = Medecin.objects.create(
        nom="Dupont",
        prenom="Jean",
        genre="M",
        email="medecin@example.com",
        matricule_medecin="123456",
        specialite=specialite,
        adresse="123 Rue de Paris", password="<PASSWORD>"
    )

    # Créer un patient pour associer aux séjours
    patient = Patient.objects.create(
        nom="Doe",
        prenom="John",
        genre="M",
        email="patient@example.com",
        adresse="456 Rue de Lyon",
        password="alimahf"
    )

    specialite.refresh_from_db()
    medecin.refresh_from_db()

    # Après avoir créé specialite et medecin
    assert Specialite.objects.filter(specialite_id=specialite.specialite_id).exists(), "Specialite introuvable"
    assert Medecin.objects.filter(id=medecin.id).exists(), "Medecin introuvable"

    # Exécuter les requêtes après cette vérification

    # Authentifier le client en tant que patient
    client.force_login(patient)

    # URL de la vue CreateSejourView
    url = reverse('soignemoiwebsite:creer_sejour')  # Assurez-vous que 'create_sejour' est bien le nom de votre URL

    # Données du formulaire pour la création de séjour
    sejour_data = {
        "date_entree": date.today(),
        "date_sortie": date.today() + timedelta(days=1),
        "motif": "Routine check-up",
        "medecin": medecin.id,
        "specialite": specialite.specialite_id,
    }

    # Fonction pour envoyer une requête de création de séjour
    def create_sejour():
        # time.sleep(1)
        print(f"Données de test envoyées : {sejour_data}")  # Affiche les données avant l'envoi
        response = client.post(url, sejour_data)
        if response.status_code == 200 and response.context_data:
            print("Erreurs de formulaire:", response.context_data.get('form').errors)
        return response.status_code

    # Simuler des requêtes concurrentes en utilisant des threads
    max_requests = 10  # 10 requêtes pour dépasser la limite de 5
    with ThreadPoolExecutor(max_workers=max_requests) as executor:
        results = list(executor.submit(create_sejour) for _ in range(max_requests))

    results = [future.result() for future in results]

    # Compter les séjours effectivement créés pour ce médecin
    sejour_count = Sejour.objects.filter(medecin=medecin).count()

    # Afficher les résultats des requêtes pour analyser les erreurs
    for status_code in results:
        if status_code != 302:
            print("Erreur : Le code de statut n'est pas 302, vérifiez les logs")

    # Assert pour vérifier que le nombre de séjours n'a pas dépassé 5
    assert sejour_count <= 5, f"Nombre de séjours créé {sejour_count}, ce qui dépasse la limite de 5."

    # Affichage optionnel pour les logs de test
    print(f"Nombre de séjours créés: {sejour_count}")
