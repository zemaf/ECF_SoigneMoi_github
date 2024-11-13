from django.urls import path
from .views import SoigneMoiWebsiteView, new_get_medecins_par_specialite, creer_sejour, CreerSejourView, RegisterView, login_user, logout_user, SejourView

app_name = 'soignemoiwebsite'

urlpatterns = [
    path('accueil/', SoigneMoiWebsiteView.as_view(), name='home'),
    # path('creer_sejour/', creer_sejour, name='creer_sejour'),
    path('creer_sejour/', CreerSejourView.as_view(), name='creer_sejour'),
    path('inscription/', RegisterView.as_view(), name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', SejourView.as_view(), name='profile'),
    path('get_medecins/<int:specialite_id>/', new_get_medecins_par_specialite, name='get_medecins_par_specialite'),
]
