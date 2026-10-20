from django.db import models
from core.models import BaseModel

class Familiar(BaseModel):
    # Opcional: podrías normalizar Parentesco creando un modelo aparte, 
    # pero si usas un campo de texto fijo según tu diagrama, queda así:
    class Parentesco(models.TextChoices):
        CONYUGE = "CONYUGE", "Cónyuge"
        HIJO = "HIJO", "Hijo/a"
        PADRE = "PADRE", "Padre"
        MADRE = "MADRE", "Madre"
        HERMANO = "HERMANO", "Hermano/a"
        TUTOR = "TUTOR", "Tutor"
        OTRO = "OTRO", "Otro"

    empleado = models.ForeignKey("empleado.Empleado", on_delete=models.CASCADE, related_name="familiar")
    persona = models.ForeignKey("persona.Persona", on_delete=models.PROTECT, related_name="vinculo_familiar",)
    parentesco = models.CharField(max_length=50, choices=Parentesco.choices)
    activo = models.BooleanField(default=True)

    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["empleado", "persona"],
                name="uq_empleado_persona_familiar",
            )
        ]

    def __str__(self):
        return (
            f"{self.persona} - "
            f"{self.get_parentesco_display()} "
            f"(Empleado: {self.empleado})"
        )


class Subsidio(BaseModel):
    tipo = models.CharField(max_length=100, unique=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Subsidio de {self.tipo} - Bs {self.monto}"


class SubsidioFamilia(BaseModel):
    familia = models.ForeignKey("familia.Familiar", on_delete=models.PROTECT, related_name="subsidio_asignado",)
    subsidio = models.ForeignKey(Subsidio, on_delete=models.PROTECT, related_name="beneficiario",)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Asignación de subsidio {self.pk}"
