# api/serializers.py
from rest_framework import serializers
from rest_framework.response import Response

from soignemoiwebsite.models import Sejour, Patient, Medecin, Prescription, Avis, Medicament, PrescriptionMedicament


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


class MedicamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicament
        fields = ['id', 'nom']


class PrescriptionMedicamentSerializer(serializers.ModelSerializer):
    medicament = MedicamentSerializer()

    class Meta:
        model = PrescriptionMedicament
        fields = ['medicament', 'posologie']


class PrescriptionSerializer(serializers.ModelSerializer):
    # On indique à Django que medicaments sera une liste et que ses enfants seront des dict en écriture seulement
    # medicaments = serializers.ListField(
    #     child=serializers.DictField(), write_only=True, required=False
    # )
    medicaments = serializers.SerializerMethodField()
    nom_patient = serializers.SerializerMethodField()  # Champ pour le nom du patient
    nom_medecin = serializers.SerializerMethodField()  # Champ pour le nom du médecin

    class Meta:
        model = Prescription
        # fields = ['prescription_id', 'user', 'date_debut_traitement', 'date_fin_traitement', 'medecin', 'medicaments']
        fields = [
            'prescription_id', 'nom_patient', 'nom_medecin',
            'date_debut_traitement', 'date_fin_traitement',
            'medicaments'
        ]
        read_only_fields = ['nom_patient', 'nom_medecin']

    def get_medicaments(self, obj):
        """
        Récupère les médicaments associés à une prescription.
        """
        relations = PrescriptionMedicament.objects.filter(prescription=obj)
        return [
            {
                "nom": relation.medicament.nom,
                "posologie": relation.posologie
            }
            for relation in relations
        ]

    def get_nom_patient(self, obj):
        """
        Récupère le nom complet du patient.
        """
        return f"{obj.user.prenom} {obj.user.nom}"

    def get_nom_medecin(self, obj):
        """
        Récupère le nom complet du médecin.
        """
        return f"Dr {obj.medecin.prenom} {obj.medecin.nom}"

    def create(self, validated_data):
        medicaments_data = validated_data.pop('medicaments', [])
        print("Médicaments reçus :", medicaments_data)

        # Créez la prescription
        prescription = super().create(validated_data)
        print("Prescription créée :", prescription)

        # Ajouter les médicaments et leurs posologies
        for medicament_data in medicaments_data:
            try:
                print("Traitement du médicament :", medicament_data)
                medicament = Medicament.objects.get(medicament_id=medicament_data['medicament_id'])
                print("Médicament trouvé :", medicament)

                # Créer la relation Prescription-Medicament
                relation = PrescriptionMedicament.objects.create(
                    prescription=prescription,
                    medicament=medicament,
                    posologie=medicament_data['posologie']
                )
                print(f"Relation créée : {relation}")
            except Medicament.DoesNotExist:
                print(f"Médicament avec medicament_id {medicament_data['medicament_id']} non trouvé")
                raise serializers.ValidationError({
                    "medicaments": f"Médicament avec medicament_id {medicament_data['medicament_id']} non trouvé."
                })

        # Retourner la prescription créée
        return prescription

    def update(self, instance, validated_data):
        medicaments_data = validated_data.pop('medicaments', [])
        prescription = super().update(instance, validated_data)

        # Mettre à jour les médicaments et leurs posologies
        for medicament_data in medicaments_data:
            medicament = Medicament.objects.get(medicament_id=medicament_data['medicament_id'])
            PrescriptionMedicament.objects.update_or_create(
                prescription=prescription,
                medicament=medicament,
                defaults={'posologie': medicament_data['posologie']}
            )

        return prescription


class AvisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avis
        fields = ['avis_id', 'user', 'libelle', 'date', 'description', 'medecin']
