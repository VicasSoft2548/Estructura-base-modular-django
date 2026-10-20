# Create your models here.
from django.db import models
from core.models import BaseModel

class PermisoLicencia(BaseModel):
    
    class TipoLicencia(models.TextChoices):
        LPC = "LPC", "LPC"
        LPV = "LPV", "LPV"
        SPP = "spp", "SPP"
        SPA = "spa", "SPA"
        CUMPLEANOS = "cumpleanos", "Cumpleaños"

    class TipoPermiso(models.TextChoices):
        PERSONAL = "personal", "Personal"
        MEDICO = "medico", "Médico"
        OTRO = "otro", "Otro"

    class UnidadTiempo(models.TextChoices):
        HORAS = "horas", "Horas"
        DIAS = "dias", "Días"
    
    #id automatico
    empleado = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT, verbose_name="Empleado")
    tipo_licencia = models.CharField(max_length=50, choices=TipoLicencia.choices, blank=True, null=True, verbose_name="Tipo de Licencia")
    tipo_permiso = models.CharField(max_length=50, choices=TipoPermiso.choices, blank=True, null=True, verbose_name="Tipo de Permiso")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    numero_permiso = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número de Permiso")
    fecha_inicio = models.DateTimeField(verbose_name="Fecha y hora de inicio")
    fecha_fin = models.DateTimeField(verbose_name="Fecha y hora de fin")
    valor = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Valor (Duración)")
    tiempo = models.CharField(max_length=10, choices=UnidadTiempo.choices, default=UnidadTiempo.DIAS, verbose_name="Unidad de Tiempo")
    jefe_area_autorizacion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Jefe de área que autoriza")
    gerente_autorizacion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Gerente que autoriza") #si aprueba él o jefe de area ya ta la aprobación pero pueden tener 2
    documentos = models.ForeignKey("documento.Documento", on_delete=models.PROTECT, verbose_name="Documento de permiso")

    class Meta:
        verbose_name = "Permiso o Licencia"
        verbose_name_plural = "Permisos y Licencias"
        ordering = ['-fecha_inicio']

    def __str__(self):
        tipo = self.tipo_licencia or self.tipo_permiso or "Permiso/Licencia"
        return f"{tipo} - {self.empleado} ({self.fecha_inicio.strftime('%d/%m/%Y')})"