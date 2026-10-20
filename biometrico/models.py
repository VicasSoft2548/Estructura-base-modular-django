# Create your models here.
from django.db import models
from instalacion.models import Instalacion
from core.models import BaseModel

class Biometrico(BaseModel):

    class TipoDispositivo(models.IntegerChoices):
        HUELLA = 1, "Huella dactilar"
        FACIAL = 2, "Reconocimiento facial"
        TARJETA = 3, "Tarjeta"
        MIXTO = 4, "Mixto"
        OTRO = 5, "Otro"

    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=30, unique=True)
    identificador_externo = models.CharField(max_length=85) #dispositivo en el software del fabricante
    tipo = models.PositiveSmallIntegerField(choices=TipoDispositivo.choices, default=TipoDispositivo.HUELLA)
    instalacion = models.ForeignKey(Instalacion, on_delete=models.PROTECT, related_name="biometrico")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        verbose_name = "Dispositivo biométrico"
        verbose_name_plural = "Dispositivos biométricos"
        constraints = [
            models.UniqueConstraint(
                fields=["instalacion", "identificador_externo"],
                name="biometrico_unico_por_instalacion"
            )
        ]
