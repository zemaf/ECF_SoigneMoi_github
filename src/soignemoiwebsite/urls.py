from django.urls import path
from .views import SoigneMoiWebsiteView, CreerSejourView


app_name = 'soignemoiwebsite'

urlpatterns = [
    path('accueil/', SoigneMoiWebsiteView.as_view(), name='home'),
    path('creer_sejour/', CreerSejourView.as_view(), name='creer_sejour'),
]