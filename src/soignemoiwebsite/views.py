from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from soignemoiwebsite.forms import CreateSejour
from soignemoiwebsite.models import Medecin


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
    specialite_id = request.GET.get('specialite')
    medecins = Medecin.objects.filter(specialite_id=specialite_id).order_by('nom')
    return JsonResponse(list(medecins.values('id', 'nom')), safe=False)
