from django.urls import path
from .views import SoigneMoiWebsiteView, get_medecins_par_specialite, creer_sejour

app_name = 'soignemoiwebsite'

urlpatterns = [
    path('accueil/', SoigneMoiWebsiteView.as_view(), name='home'),
    path('creer_sejour/', creer_sejour, name='creer_sejour'),
    path('get_medecins/<int:specialite_id>/', get_medecins_par_specialite, name='get_medecins_par_specialite'),
]