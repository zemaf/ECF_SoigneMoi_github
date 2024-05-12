from django.contrib import admin

from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'nom', 'prenom')
    list_editable = ("nom", "prenom")
    search_fields =("email", "nom", "prenom")
    list_filter = ("email",)
