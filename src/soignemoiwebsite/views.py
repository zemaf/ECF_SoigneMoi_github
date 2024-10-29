from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class SoigneMoiWebsiteView(TemplateView):
    template_name = 'soignemoiwebsite/accueil.html'
