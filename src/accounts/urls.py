from django.urls import path

from .views import signup

app_name = 'accounts'
urlpatterns = [
    path('nouveau', signup, name='signup')
]

