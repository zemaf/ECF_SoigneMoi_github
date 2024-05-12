from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # on indique le type de la clé primaire => on évite le warning W042
    name = 'accounts'
