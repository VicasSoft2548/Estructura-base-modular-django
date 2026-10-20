# Create your models here.
from django.db import models
from core.models import BaseModel

class FichaMedica(BaseModel):
    class GrupoSanguineo(models.TextChoices):
        A_POSITIVO = "A+", "A+"
        A_NEGATIVO = "A-", "A-"
        B_POSITIVO = "B+", "B+"
        B_NEGATIVO = "B-", "B-"
        AB_POSITIVO = "AB+", "AB+"
        AB_NEGATIVO = "AB-", "AB-"
        O_POSITIVO = "O+", "O+"
        O_NEGATIVO = "O-", "O-"

    empleado = models.OneToOneField("empleado.Empleado", on_delete=models.PROTECT, related_name="ficha_medica")
    tipo_sangre = models.CharField(max_length=3, choices=GrupoSanguineo.choices, blank=True)
    alergias = models.TextField(blank=True)
    observacion = models.TextField(blank=True)
    restriccion_medica = models.TextField(blank=True)

    def __str__(self):
        return f"Ficha médica de {self.empleado}"

class RegistroMedico(BaseModel):
    empleado = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT, related_name="registro_medico")
    matricula_cps = models.CharField(max_length=15, unique=True, null=True, blank=True)
    tipo_registro = models.CharField(max_length=50)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)
    diagnostico = models.TextField()
    doctor = models.CharField(max_length=150)
    observacion = models.TextField(blank=True)
    codigo_historia_clinica = models.CharField(max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return f"Registro médico ({self.tipo_registro}) de {self.empleado}"


class Enfermedad(BaseModel):
    nombre = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.nombre


class EmpleadoEnfermedad(BaseModel):
    empleado = models.ForeignKey("persona.Persona", on_delete=models.CASCADE, related_name="empleado_enfermedades")
    enfermedad = models.ForeignKey(Enfermedad, on_delete=models.CASCADE, related_name="afectados")
    observacion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.empleado} - {self.enfermedad}"


class ExamenMedico(BaseModel):
    empleado = models.ForeignKey("persona.Persona", on_delete=models.PROTECT, related_name="examenes_medicos")
    tipo_examen = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    resultado = models.TextField()
    tratamiento = models.TextField(blank=True)
    observacion = models.TextField(blank=True)
    
    def __str__(self):
        return f"Examen {self.tipo_examen} de {self.empleado}"

class Audiometria(BaseModel):
    empleado = models.ForeignKey("persona.Persona", on_delete=models.PROTECT, related_name="audiometrias")
    fecha = models.DateTimeField()
    # Resultados por Oído (Vía Aérea / Ósea en dB, o interpretación general)
    resultado_oido_derecho = models.TextField(blank=True, help_text="Resultados o diagnóstico para el oído derecho.")
    resultado_oido_izquierdo = models.TextField(blank=True, help_text="Resultados o diagnóstico para el oído izquierdo.")
    # Diagnóstico general y observaciones
    diagnostico = models.TextField(help_text="Diagnóstico audiológico final (ej. Normoyacusia, Hipoacusia conductiva, etc.)")
    observacion = models.TextField(blank=True)
    # Profesional o clínica que realizó el examen
    doctor_o_especialista = models.CharField(max_length=150, blank=True)
    # Campo opcional si manejas archivos adjuntos (como el PDF del resultado gráfico)
    archivo_resultado = models.FileField(upload_to="audiometria/", blank=True, null=True)
    documento = models.ForeignKey("documento.Documento", on_delete=models.PROTECT, related_name="documento_que_respalda_la_audiometria")

    def __str__(self):
        return f"Audiometría de {self.empleado} ({self.fecha.strftime('%d/%m/%Y')})"


class Bajas(BaseModel):
    doctor = models.CharField(max_length=150)
    empleado = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT, related_name="baja_medica")
    historia_clinica = models.ForeignKey("registro_medico.RegistroMedico", on_delete=models.PROTECT, related_name="baja_medica")
    diagnostico = models.TextField()
    dias = models.PositiveSmallIntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f"Baja médica de {self.empleado}"