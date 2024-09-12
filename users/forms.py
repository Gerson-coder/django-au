from django import forms
from django.contrib.auth.models import User
from .models import Create_members, Create_subs

class UserForm(forms.ModelForm):
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
        

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return cleaned_data

    def save(self, commit=True):
        
        user = User(
            username=self.cleaned_data['nickname'],
            email=self.cleaned_data.get('email', ''),
            first_name=self.cleaned_data.get('name', ''),
            last_name=self.cleaned_data.get('last_name', '')
        )
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        create_member = super().save(commit=False)
        create_member.user = user
        if commit:
            create_member.save()
        return create_member
    