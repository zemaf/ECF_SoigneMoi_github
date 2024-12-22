# api/serializers.py
from rest_framework import serializers
from soignemoiwebsite.models import Sejour, Patient, Medecin, Prescription, Avis


class SejourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sejour
        fields = ['sejour_id', 'date_entree', 'date_sortie', 'motif', 'user', 'specialite', 'medecin']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'nom', 'prenom', 'email', 'adresse', 'genre']


class MedecinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medecin
        fields = ['id', 'nom', 'prenom', 'specialite']


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['prescription_id', 'user', 'date_debut_traitement', 'date_fin_traitement', 'medecin']


class AvisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avis
        fields = ['avis_id', 'user', 'libelle', 'date', 'description', 'medecin']
