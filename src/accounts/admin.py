from django.contrib import admin
from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'nom', 'prenom', 'is_staff', 'is_active')
    list_editable = ("nom", "prenom", "is_staff", "is_active")
    search_fields =("email", "nom", "prenom", "is_staff", "is_active")
    list_filter = ("email",)
