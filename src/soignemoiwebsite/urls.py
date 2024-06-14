from django.urls import path

from soignemoiwebsite import views

app_name = 'soignemoiwebsite'

urlpatterns = [
    path('creer_sejour/', views.creation_sejour, name='creation-sejour'),
    path('ajax/load-medecins/', views.ajax_load_medecins, name='ajax_load_medecins'),
    path('check_patients/', views.check_nb_patients, name='check_nb_patients'),
]
