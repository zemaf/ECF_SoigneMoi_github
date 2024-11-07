from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from soignemoiwebsite.models import Medecin, Specialite


class SoigneMoiWebsiteView(TemplateView):
    template_name = 'soignemoiwebsite/accueil.html'


# class CreerSejourView(TemplateView):
#     template_name = 'soignemoiwebsite/creer_sejour.html'


def creer_sejour(request):
    specialites = Specialite.objects.all()
    return render(request, 'soignemoiwebsite/creer_sejour.html', {'specialites': specialites})


def get_medecins_par_specialite(request, specialite_id):
    medecins = Medecin.objects.filter(specialite_id=specialite_id).values('id', 'nom', 'prenom')
    # print(list(medecins))
    # django s'attendant à un dictionnaire en paramètre de JsonResponse, comme c'est une liste, on lui indique
    # de s'attendre à autre chose avec safe=False
    return JsonResponse(list(medecins), safe=False)

