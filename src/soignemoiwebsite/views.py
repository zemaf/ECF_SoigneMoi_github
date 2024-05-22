from django.http import HttpResponse
from django.shortcuts import render

from soignemoiwebsite.forms import CreateSejour


def creation_sejour(request):
    context = {}
    if request.method == 'POST':
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
