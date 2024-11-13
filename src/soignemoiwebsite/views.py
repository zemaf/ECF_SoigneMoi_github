import json
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from soignemoiwebsite.forms import SejourForm, PatientForm
from soignemoiwebsite.models import Medecin, Specialite, Sejour, Patient


class SoigneMoiWebsiteView(TemplateView):
    template_name = 'soignemoiwebsite/accueil.html'


class SejourView(LoginRequiredMixin, TemplateView):
    template_name = 'soignemoiwebsite/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sejours"] = Sejour.objects.filter(user=self.request.user)
        return context


class CreerSejourView(CreateView):
    model = Sejour
    form_class = SejourForm
    template_name = 'soignemoiwebsite/creer_sejour_check_patient.html'
    success_url = reverse_lazy('soignemoiwebsite:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['specialites'] = Specialite.objects.all()
        return context

    def form_valid(self, form):
        sejour = form.save(commit=False)
        try:
            # Django ne reconnait pas request.user comme une instance Patient, nécessaire à la création du séjour.
            # On appelle donc la méthode assign_patient du modèle séjour pour lier l'instance Patient au séjour créé.
            sejour.assign_patient(self.request.user)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

        return super().form_valid(form)


def creer_sejour(request):
    specialites = Specialite.objects.all()
    return render(request, 'soignemoiwebsite/creer_sejour.html', {'specialites': specialites})


def get_medecins_par_specialite(request, specialite_id):
    medecins = Medecin.objects.filter(specialite_id=specialite_id).values('id', 'nom', 'prenom')
    # print(list(medecins))
    # django s'attendant à un dictionnaire en paramètre de JsonResponse, comme c'est une liste, on lui indique
    # de s'attendre à autre chose avec safe=False
    return JsonResponse(list(medecins), safe=False)


def new_get_medecins_par_specialite(request, specialite_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. POST required.'}, status=400)
    medecins_disponibles = []
    if request.method == 'POST':
        body = json.loads(request.body)
        date_entree_str = body.get('date_entree')
        date_entree = timezone.datetime.strptime(date_entree_str, "%Y-%m-%d").date()

        for medecin in Medecin.objects.filter(specialite_id=specialite_id):
            # Logique de disponibilité sur la date d'entrée et date d'entrée + 1
            disponibilites = medecin.get_disponibilites(date_entree)
            if disponibilites:
                medecins_disponibles.append({
                    'id': medecin.id,
                    'nom': medecin.nom,
                    'prenom': medecin.prenom,
                    'disponible_le': disponibilites[0].strftime("%d %B %Y")  # Utilise la première date disponible
                })
                print(medecins_disponibles)

    # Préparer les données JSON pour la réponse
    data = {
        'medecins_disponibles': medecins_disponibles
    }
    return JsonResponse(data)


class RegisterView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'soignemoiwebsite/register.html'
    success_url = reverse_lazy("soignemoiwebsite:home")

    def form_valid(self, form):
        # On récupère le password, qui est un champ du formulaire donc accessible via cleaned_data
        password = form.cleaned_data.get('password')
        # pour récupérer password_confirm, on doit directement accéder à request.POST, qui contient les données brutes
        # du formulaire, avant qu’elles ne soient validées.
        password_confirm = self.request.POST.get('password_confirm')
        if password != password_confirm:
            messages.error(self.request, "Les mots de passe ne correspondent pas.")
            return self.form_invalid(form)
        
        # on crée une instance sans la sauvegarder
        user = form.save(commit=False)
        # On chiffre le mot de passe avec la méthode de django 'set_password()'
        user.set_password(form.cleaned_data['password'])
        # On sauvegarde l'utilisateur
        user.save()
        messages.success(self.request, 'Votre compte a été créé avec succès.')
        return super().form_valid(form)


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            print("user connecté")
            login(request, user)
            return redirect('soignemoiwebsite:profile')
        else:
            print("user non connecté")
    return render(request, 'soignemoiwebsite/login.html')


def logout_user(request):
    logout(request)
    return redirect('soignemoiwebsite:home')







