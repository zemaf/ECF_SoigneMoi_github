from django.urls import path

from soignemoiwebsite import views

app_name = 'soignemoiwebsite'

urlpatterns = [
    path('creer_sejour', views.creation_sejour, name='creation-sejour')
]
