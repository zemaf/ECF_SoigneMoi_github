from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class CustomManager(BaseUserManager):  # on crée un manager qui va gérer notre modèle Visiteur customisé
    # on précise les champs qui seront nécessaires pour créer un utilisateur quelconque
    def create_user(self, email='', genre='', nom='', prenom='', adresse='', password=None):
        if not email:
            raise ValueError("Vous devez entrer un email.")

        # On utilise l'attribut 'model' du manager pour définir un utilisateur en normalisant l'email
        # Cet attribut fait référence au modèle géré par le manager (CustomUser)
        user = self.model(
            email=self.normalize_email(email),
            genre=genre,
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

    nom_prenom_regex = RegexValidator(
        regex=r"^[A-Za-zÀ-ÖØ-öø-ÿ'’-]+(?: [A-Za-zÀ-ÖØ-öø-ÿ'’-]+)*$",
        message="Le prénom ne peut contenir que des lettres, espaces, apostrophes ou des tirets.",
        # code="inscription_non_valide"
    )
    adresse_regex= RegexValidator(
        regex=r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9'’,.\s]+$",
        message="Mauvais format d'adresse",
        # code="inscription_non_valide"
        )
    genre = models.CharField(max_length=3)
    nom = models.CharField(max_length=50, validators=[nom_prenom_regex],
                           help_text="uniquement lettres, espaces, apostrophes ou des tirets.",
                           blank=False)
    prenom = models.CharField(max_length=50, validators=[nom_prenom_regex],
                              help_text="uniquement lettres, espaces, apostrophes ou des tirets.",
                              blank=False)
    adresse = models.CharField(max_length=100, validators=[adresse_regex],
                               blank=False)
    email = models.EmailField(max_length=50, unique=True, blank=False)
    is_active = models.BooleanField(default=True)  # l'utilisateur a un compte actif
    is_staff = models.BooleanField(default=False)  # a accès à l'interface d'administration
    is_admin = models.BooleanField(default=False)  # a les droits d'administration ou non

    # on indique le champ qui servira de login_id (on demande le mail dans l'ECF)
    USERNAME_FIELD = "email"
    # champs requis lors de la création du superuser et on n'inclut pas "email" car défini dans USERNAME_FIELDS
    REQUIRED_FIELDS = ["nom", "prenom"]
    # on définit le manager de notre modèle CustomUser et on utilise celui qu'on a créé au-dessus
    objects = CustomManager()

    class Meta:
        verbose_name = "Utilisateur"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True