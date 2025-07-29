from django import forms

class FechaRangoForm(forms.Form):
    inicio = forms.DateField(label="Fecha inicio")
    fin = forms.DateField(label="Fecha fin")

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('inicio') and cleaned.get('fin'):
            if cleaned['inicio'] > cleaned['fin']:
                raise forms.ValidationError("Fecha inicio debe ser anterior o igual a fecha fin.")
        return cleaned
