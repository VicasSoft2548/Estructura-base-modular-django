"""
URL configuration for Sistema_SyNat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from schema_graph.views import Schema

# Puedes remover esta importación si no usas views directamente aquí
from usuarioRol import views 

urlpatterns = [
    path("", views.home, name="home"),
    path('admin/', admin.site.urls),
    path('schema/', Schema.as_view()),
    
    # ─── AGREGA ESTA LÍNEA ───
    # Esto registra tus rutas 'home' y 'signup' bajo el prefijo 'usuarios/'
    path('usuarios/', include('usuarioRol.urls')), 
]