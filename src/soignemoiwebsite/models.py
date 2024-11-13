from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import CustomUser


class Administrateur(CustomUser):
    # admin_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Patient(CustomUser):
    # user_id = models.AutoField(primary_key=True)

    # class Meta:
    #     verbose_name = "Visiteur"

    def __str__(self):
        return f" {self.genre} {self.nom} {self.prenom}"


class Specialite(models.Model):
    specialite_id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50, unique=True, verbose_name="Spécialité")

    def __str__(self):
        return f"{self.nom}"


class Medicament(models.Model):
    medicament_id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    posologie = models.TextField(max_length=255)

    def __str__(self):
        return f"Nom du médicament: {self.nom}"


class Medecin(CustomUser):
    # medecin_id = models.AutoField(primary_key=True)
    matricule_medecin = models.CharField(max_length=50, unique=True)  # matricule déterminé par l'administrateur
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE)
    admin = models.ForeignKey(Administrateur, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Dr {self.nom} {self.prenom}, spécialité : {self.specialite}"

    def get_disponibilites(self, date_entree):
        """
        Vérifie la disponibilité du médecin pour date_entree et date_entree +1 jour.
         Si ne trouve rien, cherche à +2 et +3 jours et retourne les dates de disponibilité.
        """
        disponibilites = []
        for offset in [0, 1]:
            date_intervention = date_entree + timedelta(days=offset)
            nb_patients = Sejour.objects.filter(medecin=self, date_entree=date_intervention).count()

            if nb_patients < 5:
                disponibilites.append(date_intervention)
                break
            else:
                for offset in range(2, 4):
                    date_intervention = date_entree + timedelta(days=offset)
                    nb_patients = Sejour.objects.filter(medecin=self, date_entree=date_intervention).count()

                    if nb_patients < 5:
                        disponibilites.append(date_intervention)
                        break
        return disponibilites


class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_debut_traitement = models.DateField()
    date_fin_traitement = models.DateField()
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)

    def clean(self):
        if self.date_fin_traitement < self.date_debut_traitement:
            raise ValidationError("La date de fin doit être postérieure à la date de début.")

    def __str__(self):
        return f" Ordonnance n°: {self.prescription_id} pour {self.user_id} par le Dr {self.medecin_id}."


class Avis(models.Model):
    avis_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    libelle = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField()
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Avis"  # on override le rajout du "s" (pluriel donnerait Aviss!) dans l'interface admin

    def __str__(self):
        return f"Avis rendu le {self.date} pour {self.user_id} "


class Sejour(models.Model):
    sejour_id = models.AutoField(primary_key=True)
    date_entree = models.DateField(verbose_name="Date d'entrée")
    date_sortie = models.DateField(verbose_name="Date de sortie")
    motif = models.TextField()
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE, verbose_name="Spécialité")
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)

    def clean(self):
        if self.date_entree and self.date_sortie:
            if self.date_entree >= self.date_sortie:
                raise ValidationError("La date de sortie doit être postérieure à la date d'entrée.")
        else:
            print("aucune date enregistrée!")

    def assign_patient(self, user):
        """
        On s'assure d'assigner explicitement une instance de Patient à user, car Patient et CustomUser ne sont pas liés
        par une relation OneToOne, juste par un héritage. Django ne reconnaitra ainsi pas user comme une instance Patient
        mais comme CustomUser → on récupère l'id de 'user' pour créer une instance Patient qui sera utilisée
        pour créer le séjour dans la vue CreateSejourView

        """
        try:
            patient_instance = Patient.objects.get(id=user.id)
            self.user = patient_instance
        except Patient.DoesNotExist:
            raise ValidationError("L'utilisateur n'est pas un patient valide.")

    def __str__(self):
        return (f" Séjour du {self.date_entree} au {self.date_sortie}, "
                f"avec {self.medecin}.")
