import logging

import django
import pytest
from django.db import connection
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, get_backends
from django.utils import timezone
from soignemoiwebsite.models import Sejour, Medecin, Specialite, Patient
from django.test import Client
from datetime import timedelta


@pytest.fixture
def user(db):
    return Patient.objects.create_user(
        email="marius@example.com",
        password="oyeoye",
        nom="Dupont",
        prenom="Jean",
        adresse="123 Rue Exemple",
        genre="M",
    )


@pytest.fixture
def specialite(db):
    return Specialite.objects.create(specialite_id=1, nom='Cardiologie')


@pytest.fixture
def medecin(db, specialite):
    return Medecin.objects.create(
        nom="Dupont",
        prenom="Jean",
        specialite=specialite
    )


# fixture client sans utiliser force_login
# @pytest.fixture
# def client(user):
#     client = Client()
#     client.login(username=user.email, password="<PASSWORD>")
#     return client


@pytest.fixture
def client(user):
    """
    D'une manière générale, on va utiliser force_login pour tester tout ce qui ne touche pas à la connexion en soi.
    On s'épargne ainsi tous les problèmes éventuels liés à la connexion.
    """
    client = Client()
    client.force_login(user)
    return client


def test_hachage_password(user):
    assert user.password.startswith("pbkdf2_")
    assert user.check_password("oyeoye"), "Password hash mismatch"


def test_authenticate_user(user):
    authenticated_user = authenticate(email=user.email, password='oyeoye')
    assert authenticated_user is not None, "Authentication failed"


def test_soignemoiwebsite_view(client):
    url = reverse('soignemoiwebsite:home')
    response = client.get(url)
    assert response.status_code == 200
    assert 'soignemoiwebsite/accueil.html' in [t.name for t in response.templates]


def test_sejour_view(client: Client, user):
    client.login(email=user.email, password="oyeoye")
    url = reverse('soignemoiwebsite:profile')
    response = client.get(url)
    assert response.status_code == 200
    assert 'soignemoiwebsite/profile.html' in [t.name for t in response.templates]


def test_creer_sejour_view_get(client):
    url = reverse('soignemoiwebsite:creer_sejour')
    response = client.get(url)
    assert response.status_code == 200
    assert 'soignemoiwebsite/creer_sejour_check_patient.html' in [t.name for t in response.templates]


def test_creer_sejour_view_post(client, user, specialite, medecin):
    client.login(email=user.email, password="oyeoye")
    url = reverse('soignemoiwebsite:creer_sejour')
    date_entree = timezone.now().date()
    data = {
        'date_entree': date_entree,
        'date_sortie': date_entree + timedelta(days=5),
        'motif': 'Consultation',
        'specialite': specialite.specialite_id,
        'medecin': medecin.id
    }
    response = client.post(url, data)
    assert response.status_code == 302, f"Form errors: {response.context['form'].errors}"
    assert Sejour.objects.filter(user=user, motif='Consultation').exists()


def test_get_medecins_par_specialite(client, specialite, medecin):
    url = reverse('soignemoiwebsite:get_medecins_par_specialite', args=[specialite.specialite_id])
    date_entree = (timezone.now() + timedelta(days=1)).date()
    response = client.post(url, {
        'date_entree': date_entree.strftime("%Y-%m-%d")
    }, content_type='application/json')
    assert response.status_code == 200
    response_data = response.json()
    assert 'medecins_disponibles' in response_data
    assert len(response_data['medecins_disponibles']) > 0


def test_register_view_post(client):
    url = reverse('soignemoiwebsite:register')
    data = {
        'genre': 'M',
        'nom': 'Mevlut',
        'prenom': 'Gundogu',
        'adresse': '21 jumpstreet',
        'email': 'newuser@example.com',
        'password': 'securepassword123',
        'password_confirm': 'securepassword123',
    }
    response = client.post(url, data)
    assert response.status_code == 302, f"Form errors: {response.context['form'].errors}"
    assert Patient.objects.filter(email='newuser@example.com').exists()


def test_login_user(client, user):
    client.login(email=user.email, password="oyeoye")
    url = reverse('soignemoiwebsite:login')
    data = {'email': user.email, 'password': "oyeoye"}
    response = client.post(url, data)
    assert response.status_code == 302, "login did not redirect as expected"
    assert response.url == reverse('soignemoiwebsite:profile')


def test_logout_user(client):
    url = reverse('soignemoiwebsite:logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('soignemoiwebsite:home')
