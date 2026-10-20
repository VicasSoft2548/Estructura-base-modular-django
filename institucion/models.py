# Create your models here.
from django.db import models
from core.models import BaseModel

class Institucion(BaseModel):
    class TipoInstitucion(models.IntegerChoices):
        CLIENTE =  1, "Cliente"
        CURSOS = 2, "Cursos"
        PROVEEDOR = 3, "Proveedor"
        BANCO = 4, "Banco"
        MINISTERIO = 5, "Ministerio"
        ASEGURADORA = 6, "Aseguradora"
        SERVICIO = 7, "Servicio"
        CONSULTORA = 8, "Consultora"

    #pk institucion
    tipo_institucion = models.PositiveSmallIntegerField(choices=TipoInstitucion.choices)
    nombre = models.CharField(max_length=50) 
    nit = models.CharField(max_length=25)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    activo = models.BooleanField(default=True)

class ContactoInstitucion(BaseModel):
    
    class Tratamiento(models.IntegerChoices):
        SEÑOR = 1, "Señor"
        SEÑORA = 2, "Señora"
        TIMADO = 3, "Estimado"
        TIMADA = 4, "Estimada"
    #pk id automatico
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, related_name='contactos_institucion')
    persona = models.ForeignKey("persona.Persona", on_delete=models.PROTECT) 
    cargo = models.CharField(max_length=100)
    tratamiento = models.PositiveSmallIntegerField(choices=Tratamiento.choices)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.cargo} - {self.institucion.nombre}"