from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import CreateUser, Members_eliminated, Create_subs
from .forms import UserForm, ManageUserForm
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'events.html')  # Redirigir a una URL de éxito
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

def signup_user(request):
    if request.method == 'GET':
        print('obteniendo datos')
        return render(request, 'signup.html', {'form': UserForm()})
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)  # No guarda en la base de datos aún
                user.set_password(form.cleaned_data['password'])  # Encripta la contraseña
                user.save()

                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user is None:
                    return render(request, 'signup.html', {'error': 'Ha ocurrido un error intentelo de nuevo'})
                else:
                    login(request, user)
                    return redirect('home')
            except Exception as e:
                print(f'Error al guardar el formulario {e}')
                return render(request, 'signup.html', {'form': form, 'error': 'Error en uno de los campos'})
        else:
            return render(request, 'signup.html', {'form': form, 'error': 'Error al registrarse'})

def login_user(request):
    if request.method == 'GET':
        print(request.GET)
        return render(request, 'login.html', {'form': AuthenticationForm})
    else:
        print(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'form': AuthenticationForm, 'error': 'El usuario o la contraseña es incorrecta'})
        else:
            login(request, user)
            return redirect('events')

def logout_user(request):
    logout(request)
    return redirect('home')

def members_fam(request):
    members = CreateUser.objects.all()
    return render(request, 'members_fam.html', {'members_fam': members})

def members_eliminated(request):
    members = Members_eliminated.objects.all()
    return render(request, 'members_eliminated.html', {'members_eliminated': members})

def delete_member(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes estar autenticado para realizar esta acción.')
        return redirect('login')

    if not request.user.is_sub():
        raise PermissionDenied("No tienes permiso para eliminar miembros.")

    if request.method == 'POST':
        form = ManageUserForm(request.POST)
        if form.is_valid():
            if form.delete_user():
                messages.success(request, 'El usuario ha sido eliminado correctamente.')
            else:
                messages.error(request, 'Hubo un error al intentar eliminar el usuario.')
        else:
            messages.error(request, 'Formulario inválido. Por favor revisa los campos.')
    else:
        form = ManageUserForm()

    return render(request, 'delete_member.html', {'form': form})

def restart_member(request):
    if request.method == 'GET':
        form = ManageUserForm()
        return render(request, 'restart_members.html', {'form': form})
    else:
        form = ManageUserForm(request.POST)
        if form.is_valid():
            if form.restart_user():
                return redirect('members_fam')
            else:
                return render(request, 'restart_members.html', {'form': form, 'error': 'El nickname no existe o ya fue restaurado'})
        else:
            return render(request, 'restart_members.html', {'form': form, 'error': 'Datos inválidos'})

def dashboard(request):
    if request.user.is_authenticated and request.user.is_staff:
        total_miembros_activos = CreateUser.objects.filter(is_active=True).count()
        total_miembros_eliminados = Members_eliminated.objects.count()

        context = {
            'total_miembros_activos': total_miembros_activos,
            'total_miembros_eliminados': total_miembros_eliminados,
        }
        return render(request, 'dashboard.html', context)
    else:
        messages.error(request, "No tienes los permisos necesarios para acceder a esta zona.")
        return redirect('home')

def autocomplete_nickname(request):
    if 'term' in request.GET:
        qs = CreateUser.objects.filter(nickname__icontains=request.GET.get('term'))
        nicknames = list(qs.values_list('nickname', flat=True))
        return JsonResponse(nicknames, safe=False)
    return JsonResponse([], safe=False)

def events(request):
    return render(request, 'events.html')

def ranking(request):
    return render(request, 'ranking.html')
    





    



