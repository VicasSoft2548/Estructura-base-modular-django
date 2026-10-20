from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import BaseModel
from recibo.models import Recibo

from django.db.models import F, Q

class Persona(BaseModel):
    #id automatico
    class TipoPersona(models.IntegerChoices):
        NATURAL = 1, "Persona natural"
        JURIDICA = 2, "Persona jurídica"

    class EstadoCivil(models.IntegerChoices):
        SOLTERO = 1, "Soltero/a"
        CASADO = 2, "Casado/a"
        DIVORCIADO = 3, "Divorciado/a"
        VIUDO = 4, "Viudo/a"
        UNIÓN_LIBRE = 5, "Unión Libre"

    class Sexo(models.IntegerChoices):
        FEMENINO = 1, "Femenino"
        MASCULINO = 2, "Masculino"
        OTRO = 3, "Otro /Prefiero no decir"

    tipo_persona = models.PositiveSmallIntegerField(choices=TipoPersona.choices, default=TipoPersona.NATURAL)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    ci = models.CharField(max_length=25, unique=False, blank=True)
    complemento_ci = models.CharField(max_length=5, blank=True, default="")
    sexo = models.PositiveSmallIntegerField(choices=Sexo.choices,null=True,blank=True)
    estado_civil = models.PositiveSmallIntegerField(choices=EstadoCivil.choices,null=True,blank=True)
    # Relación de una persona con otras personas, por ejemplo familiar.
    fecha_nacimiento = models.DateField(null=True, blank=True)
    lugar_nacimiento = models.PositiveSmallIntegerField(choices=Recibo.Lugar.choices, null=True, blank=True,) #sacar de otro modulo class o crear diccionario talvez o crear modulo de diccionarios o tabla de diccionarios de todos los modulos maybe
    foto = models.ImageField(upload_to="persona/", null=True, blank=True,)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["apellido", "nombre"]
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

    def __str__(self):
        return f"{self.nombre} {self.apellido}".strip()

class PersonaRol(BaseModel):

    class Tipo(models.IntegerChoices):
        REFERENTE = 1, "Referente"
        FAMILIAR = 2, "Familiar"
        ACCIONISTA = 3, "Accionista"
        EJECUTIVO_CUENTA = 4, "Ejecutivo de cuenta"
        NOTARIA = 5, "Notaría"
        ABOGADO = 6, "Abogado"
        EMPLEADO = 7, "Empleado"
        GERENTE = 8, "Gerente"
        ASISTENTE_GERENTE = 9, "Asistente de gerente"
        PRACTICANTE = 10, "Practicante"
        PASANTE = 11, "Pasante"
        EVENTUAL = 12, "Trabajador eventual"
        CLIENTE = 13, "Cliente"
        PROVEEDOR = 14, "Proveedor"
        OTRO = 99, "Otro"

    class EstadoRol(models.TextChoices):
        ACTIVO = "ACTIVO", "Activo"
        FINALIZADO = "FINALIZADO", "Finalizado"
        SUSPENDIDO = "SUSPENDIDO", "Suspendido"
        FALLECIDO = "FALLECIDO", "Fallecido"
        ELIMINADO = "ELIMINADO", "Eliminado"

    persona = models.ForeignKey(Persona, on_delete=models.PROTECT, related_name="rol",)
    tipo = models.PositiveSmallIntegerField(choices=Tipo.choices)
    organizacion = models.CharField(max_length=200, blank=True, default="",)
    fecha_inicio = models.DateField(null=True, blank=True,)
    fecha_fin = models.DateField(null=True, blank=True,)
    estado = models.CharField(max_length=15, choices=EstadoRol.choices, default=EstadoRol.ACTIVO,)
    observaciones = models.TextField(blank=True,default="")

    class Meta:
        ordering = ["persona__apellido", "tipo"]
        verbose_name = "Rol de persona"
        verbose_name_plural = "Roles de personas"
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(fecha_fin__isnull=True)
                    | models.Q(fecha_inicio__isnull=True)
                    | models.Q(fecha_fin__gte=models.F("fecha_inicio"))
                ),
                name="persona_rol_fecha_valida",
            )
        ]

    def __str__(self):
        return f"{self.persona} - {self.get_tipo_display()}"

##si una persona fue alguna vez practicante o eventual o pasante debe existir antecedentes como de buena conducta puntualidad habilidades, horas trabajadas, bajo quien estaba, que requisitos se puede tomar en cuenta en adelante
class AntecedenteLaboral(BaseModel):
    """
    Historial de una experiencia laboral o formativa.
    Guarda los datos comunes, las evaluaciones y la documentación.
    """

    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente de inicio"
        EN_CURSO = "EN_CURSO", "En curso"
        FINALIZADO = "FINALIZADO", "Finalizado"
        RETIRADO = "RETIRADO", "Retirado"
        SUSPENDIDO = "SUSPENDIDO", "Suspendido"

    persona = models.ForeignKey(Persona,on_delete=models.PROTECT,related_name="antecedentes_laborales",)
    institucion = models.ForeignKey("institucion.Institucion",on_delete=models.PROTECT,related_name="antecedentes_laborales",)
    cargo = models.CharField(max_length=150)

    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)

    supervisor = models.ForeignKey("persona.Persona",on_delete=models.PROTECT,null=True,blank=True,related_name="experiencias_supervisadas",)
    supervisor_externo = models.CharField(max_length=200,blank=True,default="",)

    horas_acordadas = models.PositiveIntegerField(null=True, blank=True)
    horas_trabajadas = models.PositiveIntegerField(null=True, blank=True)

    responsabilidades = models.TextField(blank=True, default="")
    habilidades = models.TextField(blank=True, default="")
    logros = models.TextField(blank=True, default="")

    cumplimiento = models.PositiveSmallIntegerField(null=True, blank=True,validators=[MinValueValidator(1), MaxValueValidator(5)],)
    calidad_trabajo = models.PositiveSmallIntegerField(null=True, blank=True,validators=[MinValueValidator(1), MaxValueValidator(5)],)
    trabajo_equipo = models.PositiveSmallIntegerField(null=True, blank=True,validators=[MinValueValidator(1), MaxValueValidator(5)],)
    iniciativa = models.PositiveSmallIntegerField(null=True, blank=True,validators=[MinValueValidator(1), MaxValueValidator(5)],)
    conocimientos_tecnicos = models.PositiveSmallIntegerField(null=True, blank=True,validators=[MinValueValidator(1), MaxValueValidator(5)],)

    evaluador = models.ForeignKey("persona.Persona",on_delete=models.PROTECT,null=True,blank=True,related_name="evaluaciones_laborales_realizadas",)

    promedio_evaluacion = models.DecimalField(max_digits=3,decimal_places=2,null=True,blank=True,editable=False,)

    puede_recontratarse = models.BooleanField(null=True, blank=True)
    justificacion_decision = models.TextField(blank=True, default="")
    motivo_salida = models.CharField(max_length=250, blank=True, default="")
    fortalezas = models.TextField(blank=True, default="")
    aspectos_de_mejora = models.TextField(blank=True, default="")
    observaciones = models.TextField(blank=True, default="")

    estado = models.CharField(max_length=12,choices=Estado.choices,default=Estado.PENDIENTE,db_index=True,)

    documento = models.ForeignKey("documento.Documento",on_delete=models.PROTECT,null=True,blank=True,related_name="antecedentes_laborales",)

    activo = models.BooleanField(default=True)

    def calcular_promedio(self):
        criterios = [
            self.cumplimiento,
            self.calidad_trabajo,
            self.trabajo_equipo,
            self.iniciativa,
            self.conocimientos_tecnicos,
        ]

        valores = [
            Decimal(str(valor))
            for valor in criterios
            if valor is not None
        ]

        if not valores:
            return None

        promedio = sum(valores, Decimal("0")) / Decimal(len(valores))

        return promedio.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    def save(self, *args, **kwargs):
        self.promedio_evaluacion = self.calcular_promedio()

        update_fields = kwargs.get("update_fields")
        if update_fields is not None:
            kwargs["update_fields"] = set(update_fields) | {
                "promedio_evaluacion"
            }

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-fecha_inicio"]
        verbose_name = "Antecedente laboral"
        verbose_name_plural = "Antecedentes laborales"
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(fecha_inicio__isnull=True)
                    | Q(fecha_fin__isnull=True)
                    | Q(fecha_fin__gte=F("fecha_inicio"))
                ),
                name="antecedente_fechas_validas",
            ),
            models.CheckConstraint(
                condition=(
                    Q(horas_trabajadas__isnull=True)
                    | Q(horas_acordadas__isnull=True)
                    | Q(horas_trabajadas__lte=F("horas_acordadas"))
                ),
                name="antecedente_horas_validas",
            ),
        ]

    def __str__(self):
        return f"{self.persona} - {self.cargo}"


class Practicante(BaseModel):
    """
    Detalles específicos de una práctica, pasantía o modalidad similar.
    Cada registro corresponde a un antecedente laboral.
    """

    class Modalidad(models.IntegerChoices):
        PRACTICA = 1, "Práctica"
        PASANTIA = 2, "Pasantía"
        EVENTUAL = 3, "Trabajo eventual"
        CONTRATO = 4, "Contrato laboral"
        CONSULTORIA = 5, "Consultoría"
        VOLUNTARIADO = 6, "Voluntariado"
        OTRO = 99, "Otro"

    antecedente = models.OneToOneField(AntecedenteLaboral,on_delete=models.PROTECT,related_name="detalle_practicante",)

    modalidad = models.PositiveSmallIntegerField(choices=Modalidad.choices,)

    class Meta:
        verbose_name = "Detalle de práctica o pasantía"
        verbose_name_plural = "Detalles de prácticas y pasantías"

    def __str__(self):
        return f"{self.antecedente.persona} - {self.get_modalidad_display()}"