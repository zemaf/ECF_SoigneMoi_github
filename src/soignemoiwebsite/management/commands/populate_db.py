from django.core.management import BaseCommand
from django.utils import timezone
from faker import Faker
from soignemoiwebsite.models import Patient, Sejour, Specialite, Medecin


class Command(BaseCommand):
    help = 'générer des données fictives basées sur les modèles de la base de données'

    def handle(self, *args, **kwargs):
        fake = Faker()
        patients = []
        for _ in range(20):
            patient = Patient.objects.create(
                email=fake.unique.email(),
                genre=fake.random_element(['Mr', 'Mme', 'Mrs', 'M']),
                nom=fake.first_name(),
                prenom=fake.last_name(),
                adresse=fake.address(),
                password=fake.password()
            )
            patients.append((patient.email, patient.password))

        # Afficher les mots de passe en clair des patients
        for email, password in patients:
            print(f"Patient: {email}, Password: {password}")

        # Étape 2 : Créer 5 spécialités
        specialites = ["Anesthésie", "Cardiologie", "Orthopédie", "Psychiatrie", "Ophtalmologie"]
        specialite_objs = [Specialite.objects.get_or_create(nom=nom)[0] for nom in specialites]

        # Étape 3 : Associer 1 médecin par spécialité
        for specialite in specialite_objs:
            medecin = Medecin.objects.create(
                email=fake.unique.email(),
                genre=fake.random_element(['M', 'F']),
                nom=fake.last_name(),
                prenom=fake.first_name(),
                adresse=fake.address(),
                matricule_medecin=fake.unique.bothify(text='MED#####'),
                specialite=specialite,
            )
            medecin.set_password("default_password")
            medecin.save()

            print(f"Médecin: {medecin.nom} {medecin.prenom}, "
                  f"Spécialité: {specialite.nom}, Password: {medecin.password}")

        self.stdout.write(self.style.SUCCESS("Database populated with fake data"))
