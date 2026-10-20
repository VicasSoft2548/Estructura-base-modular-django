# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator
from core.models import BaseModel

class EstadoImportacion(models.TextChoices):
    PENDIENTE = "PENDIENTE", "Pendiente"
    PROCESANDO = "PROCESANDO", "Procesando"
    COMPLETADA = "COMPLETADA", "Completada"
    CON_ERRORES = "CON_ERRORES", "Completada con errores"
    ERROR = "ERROR", "Error"


class EstadoConciliacion(models.TextChoices):
    PENDIENTE = "PENDIENTE", "Pendiente"
    APLICADA = "APLICADA", "Aplicada"
    ANULADA = "ANULADA", "Anulada"


class Cliente(BaseModel):
    #id automatico
    institucion = models.ForeignKey("institucion.Institucion", on_delete=models.PROTECT, related_name="clientes")
    abreviatura = models.CharField(max_length=30, unique=True)
    nit = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ["abreviatura"]

    def __str__(self):
        return self.abreviatura


class Importaciones(BaseModel):
    #id automatico
    nombre_archivo = models.CharField(max_length=255)
    hash_archivo = models.CharField(max_length=64, db_index=True)
    tipo_archivo = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, choices=EstadoImportacion.choices, default=EstadoImportacion.PENDIENTE,db_index=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)

    filas_leidas = models.PositiveIntegerField(default=0)
    filas_insertadas = models.PositiveIntegerField(default=0)
    filas_actualizadas = models.PositiveIntegerField(default=0)
    filas_duplicadas = models.PositiveIntegerField(default=0)
    filas_omitidas = models.PositiveIntegerField(default=0)
    filas_error = models.PositiveIntegerField(default=0)

    cantidad_movimientos = models.PositiveIntegerField(default=0)
    cantidad_empresas = models.PositiveIntegerField(default=0)

    mensaje_error = models.TextField(blank=True, default="")
    ruta_respaldo = models.CharField(max_length=500, blank=True, default="")

    class Meta:
        verbose_name = "Importación"
        verbose_name_plural = "Importaciones"
        ordering = ["-id"]

    def __str__(self):
        return self.nombre_archivo

class BcbTipoCambio(BaseModel):
    fecha = models.DateField(db_index=True)
    tipo_cambio = models.DecimalField(max_digits=12, decimal_places=6, validators=[MinValueValidator(0)])
    tipo_cambio_compra = models.DecimalField(max_digits=12, decimal_places=6, validators=[MinValueValidator(0)])
    tipo_cambio_venta = models.DecimalField(max_digits=12, decimal_places=6, validators=[MinValueValidator(0)])
    origen = models.CharField(max_length=150)
    nota = models.TextField(blank=True, default="") #sincronizado desde la tabla histórico #TCO oficial vigente BCB

    class Meta:
        verbose_name = "Tipo de cambio BCB"
        verbose_name_plural = "Tipos de cambio BCB"
        constraints = [
            models.UniqueConstraint(
                fields=["fecha", "origen"],
                name="uq_bcb_fecha_origen",
            )
        ]
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.fecha} - {self.tipo_cambio}"

class ReglasConciliacion(BaseModel):
    class Accion(models.TextChoices):
        EXCLUIR = "EXCLUIR", "Excluir"
        INCLUIR = "INCLUIR", "Incluir"
        CLASIFICAR = "CLASIFICAR", "Clasificar"
        REVISAR = "REVISAR", "Requiere revisión"

    #id automatico
    nombre = models.CharField(max_length=150) #pago de intereses, poner en exclusión algunas manualmente
    campo = models.CharField(max_length=100)
    patron = models.CharField(max_length=255) #PAGO DE INTERES
    accion = models.CharField(max_length=20, choices=Accion.choices) #Excluir
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    prioridad = models.PositiveSmallIntegerField(default=100, db_index=True) #10
    activo  = models.BooleanField(default=True)#boolean
    nota  = models.TextField(blank=True, default="")#Mantiene el movimiento visible en Extracto pero lo excluye de la conciliación.

    class Meta:
        ordering = ["prioridad", "id"]

    def __str__(self):
        return self.nombre

class RegistroAuditoria(BaseModel):
    #id automatico
    accion = models.CharField(max_length=50, db_index=True)
    tipo_entidad = models.CharField(max_length=100, db_index=True)
    entidad = models.CharField(max_length=100, db_index=True)
    resumen = models.CharField(max_length=255)
    valor_anterior = models.JSONField(null=True, blank=True)
    valor_nuevo = models.JSONField(null=True, blank=True)
    detalles = models.JSONField(null=True, blank=True)
    # Relación definida después, cuando se declara Importaciones.
    # Se incorpora mediante el modelo de importaciones más abajo.
    importacion = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        ordering = ["-id"]
    
class MovimientosCartera(BaseModel):
    #id automatico
    codigo = models.CharField(max_length=100, db_index=True)
    categoria = models.CharField(max_length=200, db_index=True)
    lado = models.CharField(max_length=10)

    # Pendiente: sustituir por FK cuando se confirme el modelo Empresa.
    empresa = models.CharField(max_length=50, db_index=True)
    fecha_movimiento = models.DateField(db_index=True) #calcular fecha vencimiento aumentando un mes
    fecha_vencimiento = models.DateField(null=True, blank=True, db_index=True,)
    monto = models.DecimalField(max_digits=18, decimal_places=2, validators=[MinValueValidator(0)],)
    moneda = models.CharField(max_length=3, db_index=True)

    concepto = models.CharField(max_length=255, blank=True, default="")
    descripcion = models.TextField(blank=True, default="")

    numero_documento = models.CharField(max_length=100, blank=True, default="")
    referencia = models.CharField(max_length=150, blank=True, default="")
    codigo_transaccion = models.CharField(max_length=100, blank=True, default="")
    comprobante = models.CharField(max_length=100, blank=True, default="")
    sucursal = models.CharField(max_length=100, blank=True, default="")

    estado = models.CharField(max_length=30, db_index=True)

    apto_conciliacion = models.BooleanField(default=True)
    motivo_exclusion = models.TextField(blank=True, default="")
    
    movimiento_vinculado = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, related_name="movimeinto_relacionado")

    origen = models.CharField(max_length=50, db_index=True)
    clave_origen = models.CharField(max_length=150, blank=True, default="")
    nombre_empresa_origen = models.CharField(max_length=200, blank=True, default="")
    orden_origen = models.PositiveIntegerField(null=True, blank=True)
    importacion = models.ForeignKey(Importaciones, on_delete=models.PROTECT, null=True, blank=True, related_name="movimiento")
    nota = models.TextField(blank=True, default="")
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["-fecha_movimiento", "-id"]
        indexes = [
            models.Index(
                fields=["empresa", "fecha_movimiento"],
                name="idx_mov_empresa_fecha",
            ),
            models.Index(
                fields=["estado", "apto_conciliacion"],
                name="idx_mov_estado_apto",
            ),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.monto}{self.moneda}"

class Conciliaciones(BaseModel):
    #id automatico
    haber = models.ForeignKey(MovimientosCartera, on_delete=models.PROTECT, related_name="Conciliacion_como_haber")
    debe = models.ForeignKey(MovimientosCartera, on_delete=models.PROTECT, related_name="Conciliacion_como_debe")
    monto_aplicado = models.DecimalField(max_digits=18, decimal_places=2, validators=[MinValueValidator(0)],)
    origen = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, choices=EstadoConciliacion.choices, default=EstadoConciliacion.PENDIENTE, db_index=True,)
    fecha_aplicacion = models.DateTimeField(null=True, blank=True)
    referencia = models.CharField(max_length=150, blank=True, default="")
    codigo_transaccion = models.CharField(max_length=100, blank=True, default="")
    nota = models.TextField(blank=True, default="")

    tipo_cambio_dte = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    tipo_cambio_pago = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    tipo_cambio_vencimiento = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)

    usd_fecha_pago = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    usd_al_vencimiento = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    usd_hoy = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    erosion = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True) #Es USD al vencimiento - USD al pago

    grupo_conciliacion = models.CharField(max_length=100, blank=True, default="", db_index=True)

    activo = models.BooleanField(default=True)
    fecha_anulacion = models.DateTimeField(null=True, blank=True)
    motivo_anulacion = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["-id"]
        indexes = [
            models.Index(
                fields=["estado", "fecha_aplicacion"],
                name="idx_conc_estado_fecha",
            ),
        ]

    def __str__(self):
        return f"Conciliación {self.pk}"

class CategoriasMovimiento(BaseModel):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    prefijo = models.CharField(max_length=30, blank=True, default="")

    permite_debe = models.BooleanField(default=True)
    permite_haber = models.BooleanField(default=True)
    controla_vencimiento = models.BooleanField(default=False)

    descripcion = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
