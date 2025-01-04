
from rest_framework.routers import DefaultRouter
from .views import SejourViewSet, MedecinPatientViewSet, AvisViewSet, PrescriptionViewSet

router = DefaultRouter()
router.register(r'sejours', SejourViewSet, basename='sejour')
router.register(r'medecin', MedecinPatientViewSet, basename='medecin-patient')
router.register(r'avis', AvisViewSet, basename='avis')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')

urlpatterns = router.urls
