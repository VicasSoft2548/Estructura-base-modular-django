# Create your models here.
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator
from core.models import BaseModel

class Objeto(BaseModel):
    class Categoria(models.IntegerChoices):
        LAPTOP = 1, "Laptop"
        CELULAR = 2, "Celular"
        VEHICULO = 3, "Vehiculo"
        MONITOR = 4, "Monitor"
        HERRAMIENTA = 5, "Monitor"
        TABLET = 6, "Tablet"
        EQUIPO = 7, "Equipo"

    class Tipo(models.IntegerChoices):
        CONSUMIBLE = 1, "Consumible"
        DURADERO = 2, "Bien duradero"

    codigo = models.CharField(max_length=40, unique=True)
    descripcion = models.CharField(max_length=250)
    tipo = models.CharField(max_length=15, choices=Tipo.choices, default=Tipo.DURADERO,)
    marca = models.CharField(max_length=15)
    categoria = models.PositiveSmallIntegerField(choices=Categoria.choices)
    unidad = models.CharField(max_length=30, default="Unidad")
    cuenta_contable = models.CharField(max_length=50)
    numero_corporativo = models.CharField(max_length=30)
    serial = models.CharField(max_length=30)
    imei = models.CharField(max_length=30)
    precio_unitario_usd = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0.00"))],)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class EmpleadoObjeto(BaseModel):
    #id automatico
    empleado = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT)
    objeto = models.ForeignKey("objeto.Objeto", on_delete=models.PROTECT)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True)
    documento = models.ForeignKey("documento.Documento", on_delete=models.PROTECT)

    def __str__(self):
        return (f"{self.objeto.codigo} - " f"{self.empleado}")