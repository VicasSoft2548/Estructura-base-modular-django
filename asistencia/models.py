from django.db import models
from django.core.validators import MinValueValidator
from core.models import BaseModel

# =========================================================
# ASISTENCIA Y PERSONAL
# =========================================================

class Asistencia(BaseModel):
    biometrico = models.ManyToManyField("biometrico.Biometrico", related_name="asistencia",)
    periodo_inicio = models.DateField()
    periodo_fin = models.DateField()
    documento = models.ForeignKey("documento.Documento", on_delete=models.PROTECT, related_name="asistencia",)

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        ordering = ["-periodo_inicio"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    periodo_fin__gte=models.F("periodo_inicio")
                ),
                name="asistencia_periodo_valido",
            )
        ]

    def __str__(self):
        return f"{self.periodo_inicio} - {self.periodo_fin}"


class AsistenciaPersonal(BaseModel):
    persona_en_el_biometrico = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    biometrico = models.ForeignKey("biometrico.Biometrico", on_delete=models.PROTECT, related_name="persona_asignada",)
    empleado = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT, related_name="asignacion_biometrica",)

    class Meta:
        verbose_name = "Persona en biométrico"
        verbose_name_plural = "Personas en biométricos"
        constraints = [
            models.UniqueConstraint(
                fields=["biometrico", "persona_en_el_biometrico"],
                name="persona_unica_por_biometrico",
            )
        ]

    def __str__(self):
        return (
            f"{self.empleado} - {self.biometrico.codigo} - "
            f"{self.persona_en_el_biometrico}"
        )

class JornadaProcesada(BaseModel):
    asistencia = models.ForeignKey(Asistencia, on_delete=models.PROTECT, related_name="jornada",)
    persona_biometrica = models.ForeignKey(AsistenciaPersonal, on_delete=models.PROTECT, related_name="jornada",)
    fecha = models.DateField()
    entrada_manana = models.TimeField(null=True, blank=True)
    salida_manana = models.TimeField(null=True, blank=True)
    entrada_tarde = models.TimeField(null=True, blank=True)
    salida_tarde = models.TimeField(null=True, blank=True)
    observacion = models.TextField(blank=True, default="")
    procesada_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Jornada procesada"
        verbose_name_plural = "Jornadas procesadas"
        ordering = ["fecha"]
        constraints = [
            models.UniqueConstraint(
                fields=["asistencia", "persona_biometrica", "fecha"],
                name="jornada_unica_por_empleado_fecha",
            )
        ]

    def __str__(self):
        return f"{self.persona_biometrica} - {self.fecha}"

# =========================================================
# PERMISOS Y COMPENSACIONES
# =========================================================

class PermisoAsignacion(BaseModel):
    empleado_solicita = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT, related_name="permiso_solicitado",)
    empleado_reemplazo = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT, related_name="permiso_de_reemplazo", null=True, blank=True,)
    licencia = models.ForeignKey("licencia.PermisoLicencia", on_delete=models.PROTECT, related_name="asignacion",)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    motivo = models.TextField(blank=True, default="")

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    fecha_fin__gte=models.F("fecha_inicio")
                ),
                name="permiso_periodo_valido",
            )
        ]

    def __str__(self):
        return f"Permiso {self.pk} - Empleado {self.empleado_solicita_id}"


class CompensacionLaboral(BaseModel):
    empleado = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT, related_name="compensacion",)
    plan_trabajo_recuperacion = models.ForeignKey("plan_trabajo.PlanTrabajo", on_delete=models.PROTECT, related_name="compensacion", null=True, blank=True,)
    fecha_pactada_recuperacion = models.DateField()
    hasta = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, default="PENDIENTE")
    descripcion = models.TextField(blank=True, default="")

    def __str__(self):
        return f"Compensación {self.pk} - Empleado {self.empleado_id}"

# =========================================================
# SANCIONES
# =========================================================

class Sancion(BaseModel):
    class Estado(models.TextChoices):
        BORRADOR = "BORRADOR", "Borrador"
        PENDIENTE = "PENDIENTE", "Pendiente"
        APLICADA = "APLICADA", "Aplicada"
        ANULADA = "ANULADA", "Anulada"

    empleado = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT, related_name="sanciones",)
    fecha_emision = models.DateField()
    periodo_inicio = models.DateField()
    periodo_fin = models.DateField()
    motivo = models.TextField()
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.BORRADOR,
    )
    observacion = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Sanción"
        verbose_name_plural = "Sanciones"
        ordering = ["-fecha_emision"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    periodo_fin__gte=models.F("periodo_inicio")
                ),
                name="sancion_periodo_valido",
            )
        ]

    def __str__(self):
        return f"Sanción {self.pk} - Empleado {self.empleado_id}"


class DetalleSancion(BaseModel):
    class Tipo(models.TextChoices):
        SIN_ENTRADA = "SIN_ENTRADA", "Sin marcación de entrada"
        SIN_SALIDA = "SIN_SALIDA", "Sin marcación de salida"
        JORNADA_INCOMPLETA = "JORNADA_INCOMPLETA", "Jornada incompleta"
        OTRO = "OTRO", "Otro incumplimiento"

    sancion = models.ForeignKey(Sancion, on_delete=models.PROTECT, related_name="detalle",)
    fecha_incumplimiento = models.DateField()
    tipo = models.CharField(max_length=30, choices=Tipo.choices)
    descripcion = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Detalle de sanción"
        verbose_name_plural = "Detalles de sanción"
        ordering = ["fecha_incumplimiento"]
        constraints = [
            models.UniqueConstraint(
                fields=["sancion", "fecha_incumplimiento", "tipo"],
                name="detalle_sancion_fecha_tipo_unico",
            )
        ]

    def __str__(self):
        return f"Sanción {self.sancion_id} - {self.fecha_incumplimiento}"


# =========================================================
# HORAS EXTRA
# =========================================================

class RegistroHoraExtra(BaseModel):
    class Tipo(models.TextChoices):
        EXTRA_DIURNA = "EXTRA_DIURNA", "Extra diurna"
        EXTRA_NOCTURNA = "EXTRA_NOCTURNA", "Extra nocturna"
        OTRO = "OTRO", "Otro concepto"

    class Tratamiento(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente de decisión"
        LPC = "LPC", "Acumular en LPC"
        COMPENSAR_HORAS = "COMPENSAR_HORAS", "Compensar con horas"
        SIGUIENTE_PLANILLA = (
            "SIGUIENTE_PLANILLA",
            "Compensar en siguiente planilla",
        )
        RECONOCER = "RECONOCER", "Reconocer para liquidación"
        ANULAR = "ANULAR", "Anular"

    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente de revisión"
        APROBADA = "APROBADA", "Aprobada"
        EJECUTADA = "EJECUTADA", "Tratamiento ejecutado"
        ANULADA = "ANULADA", "Registro anulado"

    jornada = models.ForeignKey(JornadaProcesada, on_delete=models.PROTECT, related_name="hora_extra",)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    minutos = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    tratamiento = models.CharField(max_length=30, choices=Tratamiento.choices, default=Tratamiento.PENDIENTE,)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE,)
    periodo_planilla_destino = models.CharField(max_length=20, blank=True, default="",)
    importe = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)],)
    observacion = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Registro de hora extra"
        verbose_name_plural = "Registros de horas extra"
        ordering = ["jornada__fecha", "pk"]

    def __str__(self):
        return (
            f"{self.jornada} - {self.minutos} min - "
            f"{self.get_tratamiento_display()}"
        )


# =========================================================
# REGLAS DE HORARIO
# =========================================================

class ReglaHorarioLaboral(BaseModel):
    nombre = models.CharField(max_length=100)
    vigencia_desde = models.DateField()
    vigencia_hasta = models.DateField(null=True, blank=True)
    inicio_nocturno = models.TimeField()
    fin_nocturno = models.TimeField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Regla de horario laboral"
        verbose_name_plural = "Reglas de horario laboral"
        ordering = ["-vigencia_desde"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(vigencia_hasta__isnull=True)
                    | models.Q(
                        vigencia_hasta__gte=models.F("vigencia_desde")
                    )
                ),
                name="regla_horario_vigencia_valida",
            )
        ]

    def __str__(self):
        return self.nombre
