from django import forms

from soignemoiwebsite.models import Sejour, Medecin


class CreateSejour(forms.ModelForm):
    medecin = forms.ModelChoiceField(queryset=Medecin.objects.none(), required=False)

    class Meta:
        model = Sejour
        fields = ['date_entree', 'date_sortie', 'motif', 'specialite', 'medecin']
        widgets = {'motif': forms.Textarea()}

    def __init__(self, *args, **kwargs):
        super(CreateSejour, self).__init__(*args, **kwargs)
        self.fields['medecin'].queryset = Medecin.objects.none()

        if "specialite" in self.data:
            try:
                specialite_id = int(self.data.get('specialite'))
                self.fields['medecin'].queryset = Medecin.objects.filter(specialite_id=specialite_id).order_by('nom')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.specialite:
            self.fields['medecin'].queryset = self.instance.specialite.medecin_set.order_by('nom')
