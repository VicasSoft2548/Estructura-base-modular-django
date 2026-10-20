# Create your models here.
from django.db import models
from core.models import BaseModel

class contacto(BaseModel):
    class TipoContacto (models.PositiveSmallIntegerField):
        EMAIL = 1, "Email"
        TELEFONO = 2, "Teléfono"
        REUNION = 3, "Reunión" 

     # Relacion foráneas
    institucion = models.ForeignKey("institucion.Institucion", on_delete=models.CASCADE)
    contacto_institucion = models.ForeignKey("institucion.ContactoInstitucion", on_delete=models.CASCADE)
    persona = models.IntegerField()  # ID de la persona asociada
    tipo_contacto = models.CharField(max_length=50) # Ej. "Email", "Teléfono", "Reunión"
    valor = models.CharField(max_length=150)
    principal = models.BooleanField(default=False) 
    activo = models.BooleanField(default=True)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Contacto {self.tipo_contacto} - Persona {self.persona}"