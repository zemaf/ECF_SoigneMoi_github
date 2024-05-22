from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render

from accounts.models import CustomUser

# 1ʳᵉ méthode : on utilise la méthode basique avec un formulaire créé à la main dans le template signup.html
# def signup(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password1 = request.POST.get("password1")
#         password2 = request.POST.get("password2")
#         if password1 != password2:
#             return render(request, "accounts/signup.html", {"error": "Les mots de passe ne correspondent pas"})
#
#         CustomUser.objects.create_user(email=email, nom='ali', prenom='maf', adresse="en poutet", password=password1)
#         return HttpResponse(f"Bienvenue {email} qui habite Escalquens!")
#
#     return render(request, "accounts/signup.html")


# 2ᵉ méthode avec un formulaire prédéfini dans django : UserCreationForm
# Or ce modèle fait appelle au modèle User par défaut => on doit le customiser et lui indiquer notre modèle à nous
class CustomSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', )


def signup(request):
    context ={}  # on initialise notre contexte
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('vous êtes inscrit!')
        else:
            context['errors'] = form.errors  # form.errors est lui-même un dictionnaire
    form = CustomSignupForm()
    context['form'] = form  # on ajoute notre formulaire au contexte

    return render(request, "accounts/signup.html", context=context)


def profile(request):
    return HttpResponse(f"hey {request.user}")