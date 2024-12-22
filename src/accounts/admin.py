from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Champs à afficher dans l'interface admin
    list_display = ('email', 'nom', 'prenom', 'is_staff', 'is_active')
    search_fields = ('email', 'nom', 'prenom')
    list_filter = ('is_staff', 'is_active')

    # Champs pour le formulaire d'édition
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('nom', 'prenom', 'genre', 'adresse')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_admin')}),
    )

    # Champs pour le formulaire de création
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'nom', 'prenom', 'is_staff', 'is_active'),
        }),
    )

    ordering = ('email',)

    filter_horizontal = ()

