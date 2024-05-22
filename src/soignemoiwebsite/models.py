from django.db import models

from accounts.models import CustomUser


class Administrateur(CustomUser):
    admin_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Utilisateur(CustomUser):
    user_id = models.AutoField(primary_key=True)

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
    medecin_id = models.AutoField(primary_key=True)
    matricule_medecin = models.CharField(max_length=50, unique=True)  # matricule déterminé par l'administrateur qui crée le médecin
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE)
    admin = models.ForeignKey(Administrateur, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Dr {self.nom} {self.prenom}, spécialité :{self.specialite_id}"


class Intervention(models.Model):
    intervention_id = models.AutoField(primary_key=True)
    libelle_intervention = models.CharField(max_length=100)
    date_intervention = models.DateField()
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)

    def __str__(self):
        return (f"intervention n° {self.intervention_id}, en date du {self.date_intervention}:\n"
                f"patient: {self.user_id}.")


class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_debut_traitement = models.DateField()
    date_fin_traitement = models.DateField()
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)

    # class Meta:
    #     # clé primaire composée des champs user et prescription_id
    #     constraints = [
    #         models.UniqueConstraint(fields=["user", "prescription_id"], name="unique_user_prescription")
    #     ]

    def __str__(self):
        return f" Ordonnance n°: {self.prescription_id} pour {self.user_id} par le Dr {self.medecin_id}."


class Avis(models.Model):
    avis_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    libelle = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField()
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Avis"  # on override le rajout du "s" (pluriel donnerait Aviss!) dans l'interface admin
        # # clé primaire composée des champs user et avis_id
        # constraints = [
        #     models.UniqueConstraint(fields=["avis_id", "user"], name="unique_user_avis_id")
        # ]

    def __str__(self):
        return f"Avis rendu le {self.date} pour {self.user_id} "


class Sejour(models.Model):
    sejour_id = models.AutoField(primary_key=True)
    date_entree = models.DateField(verbose_name="Date d'entrée")
    date_sortie = models.DateField(verbose_name="Date de sortie")
    motif = models.TextField()
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE, verbose_name="Spécialité")

    def __str__(self):
        return f" Séjour de {self.user_id}, du {self.date_entree} au {self.date_sortie}, en {self.specialite_id}."
