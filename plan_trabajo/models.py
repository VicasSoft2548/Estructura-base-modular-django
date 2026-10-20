# Create your models here.
from django.db import models
from core.models import BaseModel

class PlanTrabajo(BaseModel):
    # Relación con Tareas (asumiendo que el modelo se llama Tarea o Tareas)
    tarea = models.ForeignKey("centro_costo.Tareas", on_delete=models.PROTECT, related_name="plan_trabajo")
    # En lugar del concatenado, usamos relacion directas (pued hacerlas opcional si aplica)
    zona = models.ForeignKey("centro_costo.ZonaOperativa", on_delete=models.PROTECT, null=True, blank=True)
    area = models.ForeignKey("centro_costo.AreaOperativa", on_delete=models.PROTECT, null=True, blank=True)
    sistema = models.ForeignKey("centro_costo.Sistema", on_delete=models.PROTECT, null=True, blank=True)
    equipo = models.ForeignKey("centro_costo.Equipo", on_delete=models.PROTECT, null=True, blank=True)
    componente = models.ForeignKey("centro_costo.Componente", on_delete=models.PROTECT, null=True, blank=True)
    # Empleados (usando el modelo Empleado)
    empleado_jefe = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT, related_name="plan_supervisado")
    empleado_asignado = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT, related_name="plan_asignado")
    # Fechas y métricas
    fecha_asignacion = models.DateField()
    fecha_elaboracion = models.DateField(auto_now_add=True)
    progresiva = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Típicamente la progresiva vial/kilometro es numérica
    unidad = models.ForeignKey("centro_costo.UnidadMedida", on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Plan {self.pk} - Tarea: {self.tarea}"

class RegistroTrabajo(BaseModel):
    plan = models.ForeignKey(PlanTrabajo, on_delete=models.PROTECT, related_name="registro")
    fecha_ejecucion = models.DateField()
    empleado_real = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT, related_name="trabajo_ejecutado")
    progresiva_real = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    observacion = models.TextField(blank=True, default="")
    se_cumplio = models.BooleanField(default=False)
    hora_empleada = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Registro ejecución {self.fecha_ejecucion} - Plan {self.plan_id}"


class RegistroEvidencia(BaseModel):
    registro_trabajo = models.ForeignKey(RegistroTrabajo, on_delete=models.CASCADE, related_name="evidencia") # Buena práctica asociarlo al registro
    url = models.URLField(max_length=500)

    def __str__(self):
        return f"Evidencia {self.pk}"
