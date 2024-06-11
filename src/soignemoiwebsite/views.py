from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from soignemoiwebsite.forms import CreateSejour
from soignemoiwebsite.models import Medecin

import json


def creation_sejour(request):
    context = {}
    print(request)
    if request.method == 'POST':
        print("yess")
        form = CreateSejour(request.POST)
        if form.is_valid():
            sejour = form
            sejour.save()
            return HttpResponse("Séjour presque créé, faut s'authentifier maintenant!")
        else:
            context['errors'] = form.errors
    form = CreateSejour()
    context['form'] = form
    return render(request, 'soignemoiwebsite/creer_sejour.html', context=context)


def ajax_load_medecins(request):
    data = json.loads(request.body)
    # print(f" voici le contenu de la requête POST : {request.body}")
    specialite_id = data.get('specialite')
    medecins = Medecin.objects.filter(specialite_id=specialite_id).order_by('nom')
    print(medecins.values())
    # django s'attendant à un dictionnaire en paramètre de JsonResponse, comme c'est une liste, on lui indique
    # de s'attendre à autre chose avec safe=False
    return JsonResponse(list(medecins.values('id', 'nom')), safe=False)

