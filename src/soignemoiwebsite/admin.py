from django.contrib import admin

from soignemoiwebsite.models import (Utilisateur, Administrateur, Medecin, Medicament, Prescription,
                                     Specialite, Sejour, Avis)


class MedecinInline(admin.TabularInline):
    model = Medecin
    extra = 1


admin.site.register(Utilisateur)
admin.site.register(Administrateur)
admin.site.register(Medecin)
admin.site.register(Medicament)
admin.site.register(Prescription)
admin.site.register(Sejour)
admin.site.register(Avis)


@admin.register(Specialite)
class SpecialiteAdmin(admin.ModelAdmin):
    inlines = [MedecinInline]



