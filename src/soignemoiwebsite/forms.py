from django import forms

from soignemoiwebsite.models import Sejour, Medecin, Specialite


class CreateSejour(forms.ModelForm):
    medecin = forms.ModelChoiceField(queryset=Medecin.objects.none(), required=False)

    class Meta:
        model = Sejour
        fields = '__all__'
        widgets = {'date_entree': forms.SelectDateWidget(years=range(2015, 2025)),
                   'date_sortie': forms.SelectDateWidget(years=range(2015, 2025)),
                   'motif': forms.Textarea()}

    def __init__(self, *args, **kwargs):
        super(CreateSejour, self).__init__(*args, **kwargs)
        self.fields['medecin'].queryset = Medecin.objects.none()
        print(self.data)

        if "specialite" in self.data.keys():
            print("yess")
            try:
                specialite_id = int(self.data.get('specialite'))
                print(f"specialité {specialite_id}")
                self.fields['medecin'].queryset = Medecin.objects.filter(specialite_id=specialite_id).order_by('nom')
                print(self.fields['medecin'].queryset)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.specialite:
            self.fields['medecin'].queryset = self.instance.specialite.medecin_set.order_by('nom')


class SpecialiteForm(forms.ModelForm):
    class Meta:
        queryset = Specialite.objects.all()
