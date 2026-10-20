# Create your models here.
from django.db import models
from core.models import BaseModel

class Agenda(BaseModel):
    #id automatico
    asunto = models.TextField(null=False)
    activo = models.BooleanField(default=True)
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_fin = models.DateField(null=True, blank=True)
    hora = models.TimeField(null=True, blank=True)
    lugar = models.TextField(blank=True, default="")
    empleados = models.ManyToManyField(
        "empleado.Empleado",
        related_name="agendas",
        blank=True
    )