from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Create_members, Members_eliminated
from .forms import UserForm
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth  import login,authenticate, logout
from django.db import IntegrityError
# Create your views here.


def home(request):

    return render(request, 'home.html')




def signup_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'events.html')  # Redirigir a una URL de éxito
    else:
        form = UserForm()

    return render(request, 'signup.html', {'form': form})






    """
     if request.method == 'GET':
        return render(request, 'signup.html', {'form': FormMember()})
    
    else:
        print(request.POST)
        form = FormMember(request.POST)
        

        if request.POST['password1'] == request.POST['password2']:

            if form.is_valid():
                 
                user = User.objects.create_user(username=apodo, password=request.POST['password1'])
                
                try:
                   
                    miembro.save()
                    login(request,user)
                    return redirect('home')
                except IntegrityError:
                    return render(request, 'signup.html', {
                    'form': form,
                    'error': 'El usuario ya existe'
                })

           
        return render(request, 'signup.html', {
            'form': form,
            'error': 'las contraseñas no coinciden'
        })
    
    
    """
   
    

def login_user(request):
    if request.method == 'GET':
        print(request.GET)
        return render (request, 'login.html', {'form': AuthenticationForm} )
        
    else:
        print(request.POST)
        user = authenticate(request, username = request.POST['username'], password= request.POST['password'])
        if user is None:
            return render(request,'login.html',{'form': AuthenticationForm, 'error':'el usuario o la contraseña es incorrecta' } )
        else:
            login(request,user)
            return redirect('events')


def logout_user(request):
    logout(request)
    
    return redirect('home')


def members_fam (request):
    members = Create_members.objects.all()
    
    return render(request,'members_fam.html', {'members_fam':members })



def members_eliminated(request):
    members = Members_eliminated.objects.all()
    return render (request, 'members_eliminated.html', {'members_eliminated': members})
    
        
    

    
def delete_member(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        reason = request.POST.get('reason')

        # Buscamos al miembro por su nickname
        try:
            member = Create_members.objects.get(nickname=nickname)
        except Create_members.DoesNotExist:
            # Mostrar error si no existe el miembro
            return render(request, 'delete_member.html', {'error': 'Miembro no encontrado'})

        # Buscamos al usuario asociado al nickname en la tabla User
        try:
            user = User.objects.get(username=nickname)
        except User.DoesNotExist:
            # Mostrar error si no existe el usuario
            return render(request, 'delete_member.html', {'error': 'Usuario no encontrado'})

        # Desactivamos el usuario para que no pueda iniciar sesión
        user.is_active = False
        user.save()

        # Crear un registro en la tabla de miembros eliminados
        Members_eliminated.objects.create(
            name=member.name,
            nickname=member.nickname,
            reason=reason,
            recruited=member.recruited,  # Asume que reclutador es un FK
            date_eliminate=timezone.now()
        )

        # Eliminar el miembro de la tabla Create_members
        member.delete()

        # Redirigir a la lista de eliminados con mensaje de éxito
        return redirect('members_eliminated')

    return render(request, 'delete_member.html')

def restart_member(request):
    if request.method == 'POST':
        
   
    

        try:
            nickname = request.POST.get('nickname')
            
            # Verificar si el usuario está en la tabla de miembros eliminados
            member_eliminated = Members_eliminated.objects.filter(nickname =nickname).first()
            print(nickname,request)

            if member_eliminated:
                member_eliminated.delete()

            
            else:
                return render(request,'restart_members.html', {'error': 'Miembro no encontrado'})

    
    
            return render(request, 'restart_members.html', {'success': 'Miembro restaurado exitosamente'})
        
        except Members_eliminated as e:
            # Mostrar error si el miembro no se encuentra
            return render(request, 'restart_members.html', {'error': str(e) })

    return render(request, 'restart_members.html')
    
    


   
def autocomplete_nickname(request):
    if 'term' in request.GET:
        qs = Create_members.objects.filter(nickname__icontains=request.GET.get('term'))
        nicknames = list(qs.values_list('nickname', flat=True))
        return JsonResponse(nicknames, safe=False)
    return JsonResponse([], safe=False)
    

def events(request):

    return render(request, 'events.html')

def ranking(request):

    return render(request, 'ranking.html')





        

    





    



