# api/views.py
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from soignemoiwebsite.models import Sejour, Patient, Medecin, Prescription, Avis
from .permissions import IsMedecin
from .serializers import SejourSerializer, PatientSerializer, MedecinSerializer, PrescriptionSerializer, AvisSerializer
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response


class SejourViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SejourSerializer
    permission_classes = [IsAuthenticated, IsMedecin]  # authentification et rôle

    def get_queryset(self):
        date_choisie = self.request.query_params.get('date', timezone.now().date())
        return Sejour.objects.filter(date_entree__gte=date_choisie)  # noqa

    @action(detail=True, methods=['get'])
    def patient_details(self, request, pk=None):
        sejour = self.get_object()
        patient = sejour.user
        serializer = PatientSerializer(patient)
        return Response(serializer.data)


class MedecinPatientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsMedecin]  # authentification et rôle

    def get_queryset(self):
        return Patient.objects.filter(sejour__medecin=self.request.user.id).distinct()


class AvisViewSet(viewsets.ModelViewSet):
    serializer_class = AvisSerializer
    permission_classes = [IsAuthenticated, IsMedecin]  # authentification et rôle

    def get_queryset(self):
        return Avis.objects.filter(medecin=self.request.user)  # noqa


class PrescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsMedecin]  # authentification et rôle

    def get_queryset(self):
        return Prescription.objects.filter(medecin=self.request.user)


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
