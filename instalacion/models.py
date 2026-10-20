# Create your models here.
from django.db import models
from core.models import BaseModel

class Instalacion(BaseModel):
    class Tipo_instalacion(models.IntegerChoices):
        EDIFICIO = 1 , "Edificio"
        OFICINA = 2, "Oficina"
        DEPOSITO = 3, "Depósito"
        SUCURSAL = 4, "Sucursal"
        TALLER = 5, "Taller"
        OTRO = 6, "Otro"

    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=30, unique=True)
    tipo_instalacion = models.PositiveSmallIntegerField(choices=Tipo_instalacion.choices)
    direccion = models.CharField(max_length=250)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"