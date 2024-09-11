from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Create_members
from .forms import FormMember
from django.contrib.auth  import login,authenticate, logout
from django.db import IntegrityError
# Create your views here.


def home(request):

    return render(request, 'home.html')




def signup_user(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': FormMember()})
    
    else:
        print(request.POST)
        form = FormMember(request.POST)
        

        if form.is_valid():
            nombre = form.cleaned_data['name']
            edad = form.cleaned_data['age']
            apodo = form.cleaned_data['nickname']
            fecha_nacimiento = form.cleaned_data['happy_birthday']
            pais = form.cleaned_data['country']
            ciudad = form.cleaned_data['city']
            estado_cpl = form.cleaned_data['cpl_status']
            modo_juego = form.cleaned_data['mode_play']
            reclutado = form.cleaned_data['recruited']
            if request.POST['password1'] == request.POST['password2']:
                try:
                    # Crear el usuario usando el nickname como username
                    user = User.objects.create_user(username=apodo, password=request.POST['password1'])
                    
                    miembro = Create_members(
                        name=nombre,
                        age=edad,
                        nickname=apodo,
                        happy_birthday=fecha_nacimiento,
                        country=pais,
                        city=ciudad,
                        cpl_status=estado_cpl,
                        mode_play=modo_juego,
                        recruited=reclutado
                        )
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
            'error': 'Las contraseñas no coinciden'
        })
    

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

def events(request):

    return render(request, 'events.html')

def ranking(request):

    return render(request, 'ranking.html')





        

    





    



