# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator
from core.models import BaseModel

class Familiar (BaseModel):
    class Parentesco (models.IntegerChoices):
        TIO = 1, "Tío"
        TIA = 2, "Tía"
        PADRE = 3, "Padre"
        MADRE = 4, "Madre"
        HIJO = 5, "Hijo"
        HIJA = 6, "Hija"
        PRIMO = 7, "Primo"
        PRIMA = 8, "Prima"
        SOBRINO = 9, "Sobrino"
        SOBRINA = 10, "Sobrina"
        HERMANO = 11, "Hermano"
        HERMANA = 12, "Hermana"
        ABUELO = 13, "Abuelo"
        ABUELA = 14, "Abuela"
        CONYUGUE = 15, "Cónyugue"

    persona_empleado = models.ForeignKey("persona.Persona",on_delete=models.PROTECT, related_name="familiar_a_cargo",) 
    familiar = models.ForeignKey("persona.Persona",on_delete=models.PROTECT, related_name="relacion_familiar",) 
    parentesco = models.PositiveSmallIntegerField(choices= Parentesco.choices)
    carpeta_familiar = models.IntegerField(validators=[MinValueValidator(1)])
    class Meta:
        verbose_name = "Familiar"
        verbose_name_plural = "Familiar"

    def __str__(self):
        return f"{self.familiar} - {self.get_Parentesco_display()}"

class Subsidio(BaseModel):
    class TipoSubsidio (models.IntegerChoices):
        PRENATAL = 1, "Prenatal"
        LACTANCIA = 2, "Lactancia"
        NATALIDAD =  3, "Natalidad"
        SEPELIO = 4, "Sepelio"

    #id automatico
    empleado = models.ForeignKey("empleado.Empleado",on_delete=models.PROTECT, related_name="Subsidio_de_empleado",) #empleado para el q se da subsidio
    persona = models.ForeignKey("persona.Persona",on_delete=models.PROTECT, related_name="Subsidio_de_persona",) #persona a la cual ta relacionada por Parentesco, 
    tipo_de_subsidio = models.PositiveSmallIntegerField(choices=TipoSubsidio.choices) #ver si crear apaarte para montos, o solo ponerlo, uno para q no se cambie 
    cite = models.CharField(max_length=25, unique=True) #codigo del subsidio
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    matricula_persona = models.ForeignKey("persona.Persona", on_delete=models.PROTECT, related_name="Matricula_de_subsidio")#pareja de empleado
    doctor = models.CharField(max_length=150)
    documento = models.ForeignKey("documento.Documento", on_delete=models.PROTECT, related_name="Subsidio")

    class Meta:
        verbose_name = "Subsidio"
        verbose_name_plural = "Subsidios"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(fecha_final__gte=models.F("fecha_inicio")),
                name="fecha_final_subsidio_mayor_igual_inicio",
            )
        ]

    def __str__(self):
        return f"{self.cite} - {self.get_tipo_de_subsidios_display()}"
