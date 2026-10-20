# Create your models here.
from django.db import models
from core.models import BaseModel

class Informe(BaseModel):
    # Tipos de informe para soportar reporte diario o mensual
    TIPO_INFORME = [
        ('DIARIO', 'Diario'),
        ('MENSUAL', 'Mensual'),
    ]

    codigo = models.CharField(max_length=50, unique=True)
    empleado = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT, related_name="informe")
    tipo = models.CharField(max_length=10, choices=TIPO_INFORME, default='DIARIO')
    fecha_generacion_informe = models.DateField()
    
    # Si el informe  mensual, pued almacenar el m/año o evaluarlo por rango de fechas
    mes = models.PositiveIntegerField(null=True, blank=True, help_text="Mes evaluado (1-12) si es mensual")
    anio = models.PositiveIntegerField(null=True, blank=True, help_text="Año evaluado si es mensual")
    estado = models.BooleanField(default=True)
    comentario_general = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return f"Informe {self.codigo} ({self.tipo})"

class InformeDetalle(BaseModel):
    informe = models.ForeignKey(Informe, on_delete=models.CASCADE, related_name="detalle")
    #  mucho más consistente vincular el detalle al RegistroTrabajo ejecutado
    registro_trabajo = models.ForeignKey("plan_trabajo.RegistroTrabajo", on_delete=models.PROTECT, related_name="informe_detalle")
    observacion = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return f"Detalle Informe {self.informe.codigo} - Reg. Trabajo {self.registro_trabajo_id}"