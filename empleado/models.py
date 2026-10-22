# Create your models here.
from django.db import models
from core.models import BaseModel

class Empleado(BaseModel):

    class TipoEmpleado(models.IntegerChoices):
        PERMANENTE = 1, "Permanente"
        EVENTUAL = 2, "Eventual"
        PRACTICANTE = 3, "Practicante"

    class Estado(models.IntegerChoices):
        VACACION = 1, "Vacacion"
        SUSPENSION = 2, "Suspensión"
        LICENCIA = 3, "Licencia"
        BAJA_MEDICA = 4, "Baja Médica"
        DISPONIBLE = 5, "Disponible"

    class Licencia(models.IntegerChoices):
        MOTOCICLETA = 1, "Motocicleta"
        PARTICULAR = 2, "Particular"
        MOTORISTA = 3, "Motorista"
        PROFIONAL_A = 4, "Profional A"
        PROFIONAL_B = 5, "Profional B"
        PROFIONAL_C = 6, "Profional C"

    #id automatico
    codigo_empleado = models.CharField(max_length=30,unique=True) #poner inicial de la persona importar persona
    usuario = models.OneToOneField("usuarioRol.Usuario", on_delete=models.PROTECT, related_name="empleado", null=True, blank=True)
    persona = models.OneToOneField("persona.Persona", on_delete=models.PROTECT, related_name="empleo")
    tipo_empleado = models.PositiveSmallIntegerField(choices=TipoEmpleado.choices)
    fecha_ingreso = models.DateField()
    fecha_salida = models.DateField(null=True, default="")
    estado = models.PositiveSmallIntegerField(choices=Estado.choices, default=Estado.DISPONIBLE)
    activo = models.BooleanField(default=True)
    cat_licencia =  models.PositiveSmallIntegerField(choices= Licencia.choices)#deberia der algo como M - Motocicleta, el num de licencia  el ci solo necito de empleados
    autorizacion_vehicular = models.BooleanField(default=False)
    numero_licencia = models.CharField(max_length=30,blank=True,default="",)
    nua_empleado = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def __str__(self):
        return self.codigo_empleado
    
class AreaLaboral(BaseModel):
    #id automatico
    nombre = models.CharField(max_length=150, unique=True)
    activo = models.BooleanField(default=True)

    def __str__ (self):
        return self.nombre

class CargoEmpleado(BaseModel):
    #id automatico
    nombre = models.CharField(max_length=150, unique=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class AsignacionLaboral(BaseModel):
    #id automatico
    empleado = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT, related_name="asignacion",)
    area = models.ForeignKey("empleado.AreaLaboral", on_delete=models.PROTECT, related_name="asignacion",)
    cargo = models.ForeignKey("empleado.CargoEmpleado", on_delete=models.PROTECT, related_name="asignacion",)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, default="")
    principal = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.empleado} - {self.cargo}"

    class Meta:
        ordering = ["-fecha_inicio"] #facilita consultar el historial laboral de cada empleado

class ContactoEmergencia(BaseModel):
    #id automatico
    empleado = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT, related_name="Empleado",)
    persona = models.ForeignKey("persona.Persona", on_delete=models.PROTECT, related_name="Contacto_de_Emergencia",)
    familiar = models.ForeignKey("familia.Familiar", on_delete=models.PROTECT, related_name="Familiar")
     