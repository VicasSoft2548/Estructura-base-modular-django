# Create your models here.
from django.db import models
from core.models import BaseModel

class Curso(BaseModel):
    institucion = models.ForeignKey("institucion.Institucion", on_delete=models.PROTECT, verbose_name="Institucion")
    empleado = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT, verbose_name="Empleado")
    nombre = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    carga_horaria = models.PositiveSmallIntegerField()
    resolucion_ministerial = models.CharField(max_length=50, blank=True,null=True, verbose_name="Resolución ministerial",)
    documento = models.ForeignKey("documento.Documento", on_delete=models.PROTECT,blank=True,null=True,verbose_name="Documento respaldatorio")
    
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.nombre} - {self.empleado}"