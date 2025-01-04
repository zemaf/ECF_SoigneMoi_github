# api/views.py
from collections import defaultdict
from datetime import datetime

from django.contrib.auth import authenticate
from django.utils.timezone import now
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from soignemoiwebsite.models import Sejour, Patient, Medecin, Prescription, Avis, Medicament, PrescriptionMedicament
from .permissions import IsMedecin
from .serializers import SejourSerializer, PatientSerializer, MedecinSerializer, PrescriptionSerializer, AvisSerializer
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response


class SejourViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Sejour.
    Gère les opérations CRUD standard ainsi que des actions personnalisées pour :
    - Récupérer les détails des patients associés aux séjours.
    - Filtrer les séjours par date.
    """
    queryset = Sejour.objects.all()  # Tous les séjours disponibles
    serializer_class = SejourSerializer  # Définit le serializer utilisé pour transformer les données

    @action(detail=True, methods=['get'], url_path='patient_detail')
    def patient_detail(self, request, pk=None):
        """
        Action personnalisée pour récupérer les détails du patient lié à un séjour.
        Accessible via : /sejours/<id>/patient_detail/
        """
        try:
            # Récupère le séjour correspondant à l'ID fourni dans l'URL
            sejour = self.get_object()

            # Récupère le patient lié au séjour sélecté
            patient = sejour.user

            # Structure les données du patient pour la réponse JSON
            patient_data = {
                'id': patient.id,
                'nom': patient.nom,
                'prenom': patient.prenom,
                'email': patient.email,
                # Ajoutez ici d'autres champs pertinents du modèle Patient
            }

            # Retourne les informations du patient
            return Response(patient_data, status=200)

        except AttributeError:
            # Si le séjour n'est pas lié à un patient
            return Response({'error': 'Aucun patient associé à ce séjour'}, status=404)

    @action(detail=False, methods=['get'], url_path='date_du_jour')
    def sejours_date_du_jour(self, request):
        """
        Récupère tous les séjours dont la date d'entrée ou de sortie est égale à la date du jour.
        Accessible via : /sejours/date_du_jour/
        """
        # Obtenir la date actuelle
        today = now().date()

        # Filtre les séjours dont la date d'entrée ou de sortie est aujourd'hui
        sejours = Sejour.objects.filter(date_entree=today) | Sejour.objects.filter(date_sortie=today)

        # Structure les données des séjours pour la réponse
        serialized_data = [
            {
                'id': sejour.id,
                'patient': {
                    'id': sejour.patient.id,
                    'nom': sejour.patient.nom,
                    'prenom': sejour.patient.prenom,
                },
                'date_entree': sejour.date_entree,
                'date_sortie': sejour.date_sortie,
                'motif': sejour.motif,
            }
            for sejour in sejours
        ]

        # Retourne la liste des séjours pour aujourd'hui avec les détails des patients
        return Response(serialized_data, status=200)

    @action(detail=False, methods=['get'], url_path='par_date')
    def sejours_par_date(self, request):
        """
        Récupère tous les séjours pour une date spécifique fournie dans la requête.
        Accessible via : /sejours/par_date/?date=YYYY-MM-DD
        """
        # Récupère la date fournie en paramètre de requête
        date_str = request.query_params.get('date', None)

        if not date_str:
            # Retourne une erreur si la date n'est pas fournie
            return Response({'error': 'Veuillez fournir une date au format YYYY-MM-DD'}, status=400)

        try:
            # Convertit la chaîne de caractères en objet datetime.date
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            # Retourne une erreur si le format de la date est incorrect
            return Response({'error': 'Le format de la date doit être YYYY-MM-DD'}, status=400)

        # Filtre les séjours pour la date sélectionnée
        sejours = Sejour.objects.filter(date_entree=selected_date) | Sejour.objects.filter(date_sortie=selected_date)

        # Structure les données des séjours pour la réponse
        serialized_data = [
            {
                'id': sejour.sejour_id,
                'patient': {
                    'id': sejour.user.id,
                    'nom': sejour.user.nom,
                    'prenom': sejour.user.prenom,
                },
                'date_entree': sejour.date_entree,
                'date_sortie': sejour.date_sortie,
                'motif': sejour.motif,
            }
            for sejour in sejours
        ]

        # Retourne la liste des séjours pour la date fournie
        return Response(serialized_data, status=200)


# class SejourViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = SejourSerializer
#     permission_classes = [IsAuthenticated, IsMedecin]  # authentification et rôle
#     # queryset = Sejour.objects.all()
#
#     def get_queryset(self):
#         date_choisie = self.request.query_params.get('date', timezone.now().date())
#         # return Sejour.objects.filter(date_entree__gte=date_choisie)
#         return Sejour.objects.filter(medecin__nom=self.request.user.nom)
#
#     @action(detail=True, methods=['get'], url_path='patient_detail')
#     # définit une action personnalisée au sein du viewset Sejour =>
#     # on ajoute une méthode pour récupérer le détail du patient d'un séjour donné (accès grâce au pk du séjour)
#     # url doit être ....api/sejours/pk/patient_detail
#     def patient_details(self, request, pk=None):
#         sejour = self.get_object()
#         patient = sejour.user
#         serializer = PatientSerializer(patient)
#         return Response(serializer.data)


class MedecinPatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les interactions entre un médecin connecté et ses patients.
    """
    serializer_class = PatientSerializer

    def get_queryset(self):
        """
        Retourne uniquement les patients du médecin connecté.
        """
        try:
            # Vérifie si l'utilisateur est un médecin
            medecin = Medecin.objects.get(pk=self.request.user.pk)
        except Medecin.DoesNotExist:
            return Patient.objects.none()  # Pas de patients pour un utilisateur non médecin

        # Retourne les patients liés au médecin via les séjours
        sejours = Sejour.objects.filter(medecin=medecin)
        return Patient.objects.filter(pk__in=[sejour.user.pk for sejour in sejours])


class AvisViewSet(viewsets.ModelViewSet):
    serializer_class = AvisSerializer
    permission_classes = [IsAuthenticated, IsMedecin]  # authentification et rôle

    def get_queryset(self):
        return Avis.objects.filter(medecin=self.request.user)

    # [^/.]+ 1 ou +ieurs caractères autres que "/" et "." → On va capturer le paramètre trouvé après rendre_avis/
    # et l'assigner à la variable patient_id
    @action(detail=False, methods=['post'], url_path='rendre_avis/(?P<patient_id>[^/.]+)')
    def rendre_avis(self, request, patient_id=None):
        """
        Permet au médecin de rédiger un avis pour un patient spécifique.
        Accessible via : /avis/rendre_avis/<patient_id>
        """
        try:
            # Vérifie que le patient existe et on assigne à user l'instance Medecin
            patient = Patient.objects.get(pk=patient_id)
            medecin = Medecin.objects.get(pk=request.user.pk)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient non trouvé'}, status=404)
        except Medecin.DoesNotExist:
            return Response({'error': 'Médecin non trouvé'}, status=403)

        # Sérialise et valide les données de l'avis
        serializer = AvisSerializer(data=request.data)
        if serializer.is_valid():
            # Enregistre ou met à jour l'avis pour le patient
            serializer.save(user=patient, medecin=medecin)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class PrescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsMedecin]  # authentification et rôle

    def get_queryset(self):
        return Prescription.objects.filter(medecin=self.request.user)

    @action(detail=False, methods=['post'], url_path='creer_prescription/(?P<patient_id>[^/.]+)')
    def creer_prescription(self, request, patient_id=None):
        """
        Permet au médecin de créer ou de modifier une prescription pour un patient spécifique.
        Accessible via : /prescriptions/creer_prescription/<patient_id>/
        """
        try:
            patient = Patient.objects.get(pk=patient_id)
            medecin = Medecin.objects.get(pk=request.user.pk)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient non trouvé'}, status=404)
        except Medecin.DoesNotExist:
            return Response({'error': 'Médecin non trouvé'}, status=403)

            # Sérialise et valide les données de la prescription
        prescription_serializer = PrescriptionSerializer(data=request.data)
        if prescription_serializer.is_valid():
            prescription = prescription_serializer.save(user=patient, medecin=medecin)
            print(f"prescription sérialisée : {prescription}")

            # Gérer les médicaments et leurs posologies
            medicaments_data = request.data.get('medicaments', [])
            for medicament_data in medicaments_data:
                medicament_id = medicament_data.get('medicament_id')
                posologie = medicament_data.get('posologie')
                print(medicament_id, posologie)

                try:
                    medicament = Medicament.objects.get(pk=medicament_id)
                except Medicament.DoesNotExist:
                    return Response({'error': f'Médicament {medicament_id} non trouvé'}, status=404)

                # Créer ou mettre à jour la relation PrescriptionMedicament
                PrescriptionMedicament.objects.update_or_create(
                    prescription=prescription,
                    medicament=medicament,
                    defaults={'posologie': posologie}
                )

            return Response(PrescriptionSerializer(prescription).data, status=200)

        return Response(prescription_serializer.errors, status=400)

    @action(detail=True, methods=['get'], url_path='voir_prescription')
    def voir_prescription(self, request, pk=None):
        """
        Permet au médecin de voir les détails d'une prescription spécifique, y compris les médicaments.
        Accessible via : /prescriptions/<prescription_id>/voir_prescription/
        """
        try:
            # Récupérer la prescription
            prescription = Prescription.objects.get(pk=pk, medecin=request.user)
        except Prescription.DoesNotExist:
            return Response({'error': 'Prescription non trouvée ou non accessible'}, status=404)

        # Récupérer les médicaments associés
        relations = PrescriptionMedicament.objects.filter(prescription=prescription)
        medicaments = [
            {
                "id": relation.medicament.medicament_id,
                "nom": relation.medicament.nom,
                "posologie": relation.posologie
            }
            for relation in relations
        ]

        # Construire les données de la prescription
        data = {
            "prescription_id": prescription.prescription_id,
            "patient": str(prescription.user),
            "date_debut_traitement": prescription.date_debut_traitement,
            "date_fin_traitement": prescription.date_fin_traitement,
            "medecin": str(prescription.medecin),
            "medicaments": medicaments,
        }

        return Response(data, status=200)

    @action(detail=False, methods=['get'], url_path='par_patient')
    def prescriptions_par_patient(self, request):
        """
        Retourne la liste des prescriptions du médecin triées par patient.
        Accessible via : /soignemoi/api/prescriptions/par_patient/
        """
        # Récupérer toutes les prescriptions du médecin connecté
        prescriptions = self.get_queryset()

        # Organiser les prescriptions par patient
        prescriptions_par_patient = defaultdict(list)
        for prescription in prescriptions:
            patient_nom = f"{prescription.user.prenom} {prescription.user.nom}"
            prescription_data = {
                "prescription_id": prescription.prescription_id,
                "date_debut_traitement": prescription.date_debut_traitement,
                "date_fin_traitement": prescription.date_fin_traitement,
                "medicaments": [
                    {
                        "nom": relation.medicament.nom,
                        "posologie": relation.posologie
                    }
                    for relation in PrescriptionMedicament.objects.filter(prescription=prescription)
                ],
            }
            prescriptions_par_patient[patient_nom].append(prescription_data)

        # Formater les données pour la réponse
        response_data = [
            {
                "patient": patient,
                "prescriptions": prescriptions,
            }
            for patient, prescriptions in prescriptions_par_patient.items()
        ]

        return Response(response_data, status=200)

    @action(detail=True, methods=['post'], url_path='update_prescription')
    def update_prescription(self, request, pk=None):
        """
        Permet au médecin de modifier une prescription existante,
        y compris les médicaments et leurs posologies.
        Accessible via : /prescriptions/<pk>/update_prescription/ car @action(detail=True...)
        """
        try:
            # Vérifie que la prescription existe
            prescription = Prescription.objects.get(pk=pk)
            print(prescription)
            # Vérifie que l'utilisateur connecté est le médecin de la prescription
            medecin = Medecin.objects.get(pk=request.user.pk)
            if prescription.medecin != medecin:
                return Response({'error': 'Non autorisé à modifier cette prescription'}, status=403)
        except Prescription.DoesNotExist:
            return Response({'error': 'Prescription non trouvée'}, status=404)
        except Medecin.DoesNotExist:
            return Response({'error': 'Médecin non trouvé'}, status=403)

        # Sérialiser et valider les données mises à jour
        serializer = self.get_serializer(prescription, data=request.data, partial=True)
        if serializer.is_valid():
            # Sauvegarder les modifications
            serializer.save()

            # Gérer les médicaments et leurs posologies
            medicaments_data = request.data.get('medicaments', [])
            for medicament_data in medicaments_data:
                medicament_id = medicament_data.get('id')
                posologie = medicament_data.get('posologie')

                try:
                    medicament = Medicament.objects.get(medicament_id=medicament_id)
                except Medicament.DoesNotExist:
                    return Response({'error': f'Médicament avec ID {medicament_id} non trouvé'}, status=404)

                # Créer ou mettre à jour la relation Prescription-Medicament
                PrescriptionMedicament.objects.update_or_create(
                    prescription=prescription,
                    medicament=medicament,
                    defaults={'posologie': posologie}
                )

            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)


class CustomObtainAuthToken(APIView):
    """
    Vue personnalisée pour obtenir un token en utilisant email et password.
    Accessible uniquement aux médecins.
    """
    permission_classes = [AllowAny]  # Autorise tout le monde à accéder à cette vue

    def post(self, request, *args, **kwargs):
        # Récupère les identifiants fournis dans la requête
        email = request.data.get('email')
        password = request.data.get('password')
        print(email, password)

        if not email or not password:
            return Response({'error': 'Email et mot de passe requis'}, status=status.HTTP_400_BAD_REQUEST)

        # Authentifie l'utilisateur

        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            # Vérifie que l'utilisateur est un médecin
            try:
                medecin = Medecin.objects.get(pk=user.pk)  # Charge l'utilisateur comme Medecin
                user = medecin
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            except Medecin.DoesNotExist:
                return Response({'error': 'Cet utilisateur n\'est pas un médecin'}, status=status.HTTP_403_FORBIDDEN)

                # Si l'authentification échoue
        return Response({'error': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)
