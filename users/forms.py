from django import forms
from .models import Create_members, Create_subs

class FormMember(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input'}),
        label='contraseña'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input'}),
        label='repite la contraseña'
    )
    happy_birthday = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'input'}),
        label='Cumpleaños'
    )
    recruited = forms.ModelChoiceField(
        queryset=Create_subs.objects.all(),
        widget=forms.Select(attrs={'class': 'input'}),
        label='Reclutado por'
    )

    class Meta:
        model = Create_members
        fields = ['name', 'age', 'nickname', 'happy_birthday', 'country', 'city', 'cpl_status', 'mode_play', 'recruited']

        # Personalización de las etiquetas
        labels = {
            'name': 'Nombre',
            'age': 'Edad',
            'nickname': 'nickname',
            'happy_birthday': 'Cumpleaños',
            'country': 'País',
            'city': 'Ciudad',
            'cpl_status': 'Estado(Couple)',
            'mode_play': 'Qué modo juegas',
            'recruited': 'Reclutado por',
        }
        # falta añadir fecha de ingreso pero solo en la base de datos

 
    