
from django import forms
from .models import Create_members, Create_subs



class FormMember(forms.ModelForm):
    password1 = forms.CharField(widget= forms.PasswordInput, label='contraseña')
    password2 = forms.CharField(widget= forms.PasswordInput, label='repite la contraseña')

    class Meta:

        model = Create_members
        fields = ['name', 'age', 'nickname','password1','password2', 'happy_birthday', 'country', 'city', 'cpl_status', 'mode_play', 'recruited']

        # Personalización de las etiquetas
        labels = {
            'name': 'Nombre',
            'age': 'Edad',
            'nickname': 'nickname',
            'happy_birthday': 'Cumpleaños',
            'country': 'País',
            'city': 'Ciudad',
            'cpl_status': 'Estado Civil',
            'mode_play': '¿Qué modo juegas?',
            'recruited': 'Reclutado por',
        }
    def clean(self):

            cleaned_data = super().clean() # obtiene toda la información del formulario (en este caso, las contraseñas y otros campos) 
            password1 = cleaned_data.get('password1') #Aquí, estás sacando las contraseñas de las invitaciones para compararla
            password2 = cleaned_data.get('password2')
 
            if password1 and password2 and password1 != password2: # si las dos contraseñas están presentes y no son iguales, entonces hay un problema".
                self.add_error('password2', 'Las contraseñas no coinciden')

    
    