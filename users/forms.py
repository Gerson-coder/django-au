from django import forms
from django.utils import timezone
from django.core.exceptions import   ValidationError
from django.contrib.auth.models import User
from .models import CreateUser, Members_eliminated


class UserForm(forms.ModelForm):


    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Repite la contraseña',widget=forms.PasswordInput)
    cumpleaños = forms.DateField(label='Cumpleaños', widget=forms.DateInput(attrs={'type':'date'}))
    nickname = forms.CharField(label='Nickname')
    edad = forms.IntegerField(label= 'Edad')

    class Meta: # establece las 
        model = CreateUser
        fields = ['username', 'password', 'password_confirm','first_name','nickname', 'edad',   'pais', 'ciudad', 'estado_cpl', 'modo_de_juego', 'reclutado_por'] # en fields solo traigo los campos que necesito

        labels ={
            'username': 'Nombre de usuario',
            
            'first_name': 'Nombre',

            }
    
        
    
        # Elimina el help_text predeterminado del campo username
        help_texts = {
            'username': None,

        }
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': 'Este campo es necesario'}
            
                


    def clean_username(self):

        username = self.cleaned_data.get('username')
        if CreateUser.objects.filter(username=username).exists():
            raise ValidationError("el usuario ya existe")
        return username

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm:
            if len(password) and len(password_confirm) < 6:
                raise ValidationError(" la contraseña tiene que tener un mínimo de 6 digitos") 

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Las contraseñas no coinciden.")
        return password_confirm
        

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        """
         if len(nickname) < 3:
            raise ValidationError("El nickname debe tener al menos 3 caracteres.")
        
        """
       
        if CreateUser.objects.filter(nickname=nickname).exists():
            raise ValidationError("Este nickname ya está en uso. Por favor elige otro.")
        
        return nickname
       

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad < 18:
            raise ValidationError("Debes tener al menos 18 años para registrarte.")
        return edad

    def clean_cumpleaños(self):
        cumpleaños = self.cleaned_data.get('cumpleaños')
        if not cumpleaños:
            raise ValidationError("El campo cumpleaños es obligatorio.")
        return cumpleaños


class ManageUserForm(forms.Form):
    nickname = forms.CharField(max_length=100)
    razon = forms.CharField(widget=forms.Textarea, label="Motivo de la eliminación", required=False)

    def delete_user(self):
        nickname = self.cleaned_data.get('nickname')
        razon = self.cleaned_data.get('razon')

        try:
            user = CreateUser.objects.get(nickname=nickname)

            # Proporcionar un valor predeterminado para cumpleaños si es None
            cumpleaños = user.cumpleaños if user.cumpleaños else timezone.now()

            # Guarda el usuario en Members_eliminated antes de eliminarlo
            Members_eliminated.objects.create(
                nombre=user.first_name,
                edad=user.edad,
                nickname=user.nickname,
                cumpleaños=cumpleaños,
                pais=user.pais,
                ciudad=user.ciudad,
                estado_cpl=user.estado_cpl,
                username=user.username,  # Guardar el nombre de usuario
                password=user.password,  # Guardar la contraseña encriptada
                modo_de_juego=user.modo_de_juego,
                razon=razon,
                reclutado_por=user.reclutado_por,
                fecha_elimiado=timezone.now(),
                is_active=False  # Marcar como inactivo
            )
            user.delete()
            print(f"Usuario {nickname} eliminado exitosamente.")
            return True
        except CreateUser.DoesNotExist:
            print(f"Usuario {nickname} no encontrado en CreateUser.")
            return False

    def restore_user(self):
        nickname = self.cleaned_data.get('nickname')

        try:
            user = Members_eliminated.objects.get(nickname=nickname)

            # Verificar si el usuario ya existe en CreateUser
            if CreateUser.objects.filter(nickname=user.nickname).exists():
                print(f"Usuario {user.nickname} ya existe en CreateUser.")
                return False

            if not user.nickname or not user.edad or not user.cumpleaños or not user.nombre:
                print("Campos requeridos faltantes.")
                return False

            # Crear usuario en CreateUser
            try:
                CreateUser.objects.create(
                    first_name=user.nombre,
                    edad=user.edad,
                    nickname=user.nickname,
                    cumpleaños=user.cumpleaños,
                    pais=user.pais,
                    ciudad=user.ciudad,
                    estado_cpl=user.estado_cpl,
                    username=user.username,  # Restaurar el nombre de usuario
                    password=user.password,  # Restaurar la contraseña encriptada
                    modo_de_juego=user.modo_de_juego,
                    reclutado_por=user.reclutado_por,
                    is_active=True  # Marcar como activo
                )
                print(f"Usuario {user.nickname} restaurado exitosamente.")
            except Exception as e:
                print(f"Error al restaurar usuario: {e}")
                return False

            user.delete()  # Eliminar el usuario de Members_eliminated
            return True
        except Members_eliminated.DoesNotExist:
            print(f"Usuario {nickname} no encontrado en Members_eliminated.")
            return False