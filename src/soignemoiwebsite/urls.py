from django.urls import path
from .views import SoigneMoiWebsiteView


app_name = 'soignemoiwebsite'

urlpatterns = [
    path('accueil/', SoigneMoiWebsiteView.as_view(), name='home'),
]