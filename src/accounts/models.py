from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomManager(BaseUserManager):  # on crée un manager qui va gérer notre modèle Visiteur customisé
    # on précise les champs qui seront nécessaires pour créer un utilisateur quelconque
    def create_user(self, email='', nom='', prenom='', adresse='', password=None):
        if not email:
            raise ValueError("Vous devez entrer un email.")

        # On utilise l'attribut 'model' du manager pour définir un utilisateur en normalisant l'email
        # Cet attribut fait référence au modèle géré par le manager (CustomUser)
        user = self.model(
            email=self.normalize_email(email),
            nom=nom,
            prenom=prenom,
            adresse=adresse,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, nom='', prenom='', password=None):
        if not email:
            raise ValueError("Vous devez entrer un email.")
        user = self.model(
            email=self.normalize_email(email),
            nom=nom,
            prenom=prenom
        )
        user.set_password(password)
        # user = self.create_user(email=email, nom=nom, prenom=prenom, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user


class CustomUser(AbstractBaseUser):  # modèle de base à compléter et comprenant le mot de passe

    nom = models.CharField(max_length=150, blank=False)
    prenom = models.CharField(max_length=150, blank=False)
    adresse = models.CharField(max_length=150, blank=False)
    email = models.EmailField(max_length=150, unique=True, blank=False)
    is_active = models.BooleanField(default=True)  # l'utilisateur a un compte actif
    is_staff = models.BooleanField(default=False)  # a accès à l'interface d'administration
    is_admin = models.BooleanField(default=False)  # a les droits d'administration ou non

    USERNAME_FIELD = "email"  # on indique le champ qui servira de login_id (on demande le mail dans l'ECF)
    REQUIRED_FIELDS = ["nom", "prenom"]  # champs requis lors de la création du superuser et on n'inclut pas "email" car défini dans USERNAME_FIELDS

    objects = CustomManager()  # on définit le manager de notre modèle CustomUser et on utilise celui qu'on a créé au-dessus.

    class Meta:
        verbose_name = "Utilisateur"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True