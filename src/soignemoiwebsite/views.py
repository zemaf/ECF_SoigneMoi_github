from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from soignemoiwebsite.forms import CreateSejour
from soignemoiwebsite.models import Medecin

import json


def creation_sejour(request):
    context = {}
    if request.method == 'POST':
        print(request.POST)
        form = CreateSejour(request.POST)
        if form.is_valid():
            sejour = form
            sejour.save()
            print("le séjour a été enregistré en base.")
            return HttpResponse("Séjour presque créé, faut s'authentifier maintenant!")
        else:
            print("on a eu un soucis!")
            context['errors'] = form.errors
            for field, errors in form.errors.items():
                print(f"error on {field}: {errors}")
    form = CreateSejour()
    context['form'] = form
    return render(request, 'soignemoiwebsite/creer_sejour.html', context=context)


def ajax_load_medecins(request):
    data = json.loads(request.body)
    # print(f" voici le contenu de la requête POST : {request.body}")
    specialite_id = data.get('specialite')
    medecins = Medecin.objects.filter(specialite_id=specialite_id).order_by('nom')
    # print(medecins.values())
    # django s'attendant à un dictionnaire en paramètre de JsonResponse, comme c'est une liste, on lui indique
    # de s'attendre à autre chose avec safe=False
    return JsonResponse(list(medecins.values('id', 'nom')), safe=False)


def check_nb_patients(request):
    data = json.loads(request.body)
    medecin_id = data.get('medecin')
    if medecin_id:

        return JsonResponse({'medecin_id': medecin_id})
    return JsonResponse({'error': 'Pas de médecin'}, status=400)

