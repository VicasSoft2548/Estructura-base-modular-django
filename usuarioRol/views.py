from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#la linea de abajo es para obtener mi metodo personalizado de usuario para que pueda usar lo del model
from django.contrib.auth import get_user_model 
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required ##poner en cada uno de los views

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):

    
    if request.method == 'GET':
        return render(request, 'signup.html',{
        'form': UserCreationForm
    })
    print(request.POST)
    if request.POST['password1'] == request.POST['password2']:
        try:
            #register user
            UsuarioPersonalizado = get_user_model()
            user = UsuarioPersonalizado.objects.create_user(correo=request.POST['correo'], password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect('dashboard')
        except IntegrityError:
            return render(request, 'signup.html',{
                    'form': UserCreationForm, 
                    "error":'El correo electrónico ya existe'
                })
        #except Exception as error:  # <-- Cambia esto temporalmente para ver el error real
            #  return HttpResponse(f'El error real es: {error}')
    return render(request, 'signup.html',{
        'form': UserCreationForm, 
        "error":'Las contraseñas no coinciden'
    })

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            # Verificar el estado de la cuenta antes de iniciar sesión
            if user.estado_cuenta != user.EstadoCuenta.ACTIVA:
                return render(request, "login.html", {
                    "form": form,
                    "error": "Tu cuenta no está activa. Contacta al administrador."
                })

            login(request, user)
            return redirect("dashboard")

        return render(request, "login.html", {
            "form": form,
            "error": "El correo o la contraseña son incorrectos."
        })

    form = AuthenticationForm(request)

    return render(request, "login.html", {
        "form": form
    })



@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def signout(request):
    logout(request)
    return redirect('home')