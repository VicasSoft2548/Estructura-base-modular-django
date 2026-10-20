# Create your models here.
from django.db import models
from django.conf import settings
from core.models import BaseModel

class Almacen(BaseModel):
    #id automatico
    nombre = models.TextField(null=False)
    codigo = models.CharField(max_length=30, unique=True)
    instalacion = models.ForeignKey("instalacion.Instalacion",on_delete=models.PROTECT, related_name="almacen",)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="almacen_responsable",null=True,blank=True,)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
