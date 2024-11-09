from django import forms
from .models import Sejour, Patient


class SejourForm(forms.ModelForm):
    class Meta:
        model = Sejour
        fields = ['date_entree', 'date_sortie', 'motif', 'specialite', 'medecin']  # Champs affichés dans le formulaire


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['genre', 'nom', 'prenom', 'adresse', 'email', 'password']
