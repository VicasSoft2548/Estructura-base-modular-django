# Create your models here.
from django.db import models
from core.models import BaseModel

class UnidadMedida(BaseModel):
    #id automatico
    nombre = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre

class Cuenta(BaseModel):
    #id automatico
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre


class Sistema(BaseModel):
    #id automatico
    cuentacontable = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name='sistema')
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    unidad = models.IntegerField() # Replace with appropriate ForeignKey if linked to Unidad

    def __str__(self):
        return self.nombre


class AreaOperativa(BaseModel):
    #id automatico
    sistema = models.ForeignKey(Sistema, on_delete=models.PROTECT, related_name='area_operativa')
    nombre = models.CharField(max_length=150)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.nombre


class ZonaOperativa(BaseModel):
    area_operativa = models.ForeignKey(AreaOperativa, on_delete=models.PROTECT, related_name='zona_operativa')
    unidad = models.IntegerField() # Replace with appropriate ForeignKey if linked to Unidad
    nombre = models.CharField(max_length=150)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.nombre


class Equipo(BaseModel):
    sistema = models.ForeignKey(Sistema, on_delete=models.PROTECT, related_name='equipo')
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    unidad = models.IntegerField()

    def __str__(self):
        return self.nombre


class Componente(BaseModel):
    equipo = models.ForeignKey(Equipo, on_delete=models.PROTECT, related_name='componente')
    nombre = models.CharField(max_length=150)
    unidad = models.IntegerField()
    cantidad = models.IntegerField()

    def __str__(self):
        return self.nombre

class Tareas(BaseModel):
    #id automatico
    codigo = models.CharField(max_length=25)
    nombre = models.CharField(max_length=25)
    detalle = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)

    