# accionista/models.py
from decimal import Decimal
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import (MinValueValidator,MaxValueValidator,)
from django.db import models
from django.db.models import Sum
from django.utils import timezone

from core.models import BaseModel

class Accionista(BaseModel):
    class Estado(models.TextChoices):
        ACTIVO = "ACTIVO", "Activo"
        INACTIVO = "INACTIVO", "Inactivo"

    persona = models.OneToOneField("persona.Persona", on_delete=models.PROTECT, related_name="registro_accionista",)
    codigo = models.CharField(max_length=20, unique=True, help_text="Ejemplo: ACC-00125",)
    fecha_alta = models.DateField(default=timezone.localdate)
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.ACTIVO, db_index=True,)
    observaciones = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["codigo"]

    def clean(self):
        super().clean()
        if not self.persona_id:
            return
        
        # Validación simplificada de naturaleza de persona
        p = self.persona
        if p.naturaleza == "JURIDICA" and not p.razon_social.strip():
            raise ValidationError({"persona": "La persona jurídica debe tener razón social."})
        if p.naturaleza == "NATURAL" and not p.nombre.strip():
            raise ValidationError({"persona": "La persona natural debe tener nombre."})

    def __str__(self):
        return f"{self.codigo} - {self.persona}"
class TipoAccion(BaseModel):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    valor_nominal = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    moneda = models.CharField(max_length=3, default="BOB")
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class MovimientoAccionario(BaseModel):
    class Tipo(models.TextChoices):
        EMISION = "EMISION", "Emisión"
        ADQUISICION = "ADQUISICION", "Adquisición"
        TRANSFERENCIA_ENTRADA = "TRANSFERENCIA_ENTRADA", "Transferencia recibida"
        TRANSFERENCIA_SALIDA = "TRANSFERENCIA_SALIDA", "Transferencia entregada"
        CANCELACION = "CANCELACION", "Cancelación"
        AJUSTE_POSITIVO = "AJUSTE_POSITIVO", "Ajuste positivo"
        AJUSTE_NEGATIVO = "AJUSTE_NEGATIVO", "Ajuste negativo"

    accionista = models.ForeignKey(Accionista, on_delete=models.PROTECT, related_name="movimientos")
    tipo_accion = models.ForeignKey(TipoAccion, on_delete=models.PROTECT, related_name="movimientos")
    tipo = models.CharField(max_length=25, choices=Tipo.choices)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    fecha = models.DateField(default=timezone.localdate, db_index=True)
    
    referencia_operacion = models.UUIDField(default=uuid4, editable=False, db_index=True)
    contraparte = models.ForeignKey(Accionista, on_delete=models.PROTECT, related_name="movimientos_contraparte", null=True, blank=True)
    documento_referencia = models.CharField(max_length=100, blank=True, default="")
    observaciones = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["fecha", "id"]
        indexes = [models.Index(fields=["accionista", "tipo_accion", "fecha"])]

    def clean(self):
        super().clean()
        es_transferencia = self.tipo in {self.Tipo.TRANSFERENCIA_ENTRADA, self.Tipo.TRANSFERENCIA_SALIDA}

        if es_transferencia and not self.contraparte_id:
            raise ValidationError({"contraparte": "La transferencia requiere contraparte."})
        if self.contraparte_id and self.accionista_id == self.contraparte_id:
            raise ValidationError({"contraparte": "La contraparte debe ser otro accionista."})

    @property
    def suma_acciones(self):
        POSITIVOS = {self.Tipo.EMISION, self.Tipo.ADQUISICION, self.Tipo.TRANSFERENCIA_ENTRADA, self.Tipo.AJUSTE_POSITIVO}
        NEGATIVOS = {self.Tipo.TRANSFERENCIA_SALIDA, self.Tipo.CANCELACION, self.Tipo.AJUSTE_NEGATIVO}
        
        multiplicador = 1 if self.tipo in POSITIVOS else (-1 if self.tipo in NEGATIVOS else 0)
        return self.cantidad * multiplicador


class DeclaracionDividendo(BaseModel):
    class Estado(models.TextChoices):
        BORRADOR = "BORRADOR", "Borrador"
        APROBADO = "APROBADO", "Aprobado"
        ANULADO = "ANULADO", "Anulado"

    gestion = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2200)])
    moneda = models.CharField(max_length=3, default="BOB")
    fecha_corte = models.DateField(help_text="Fecha usada para determinar quién tiene derecho al dividendo.")
    fecha_aprobacion = models.DateField(null=True, blank=True)
    numero_resolucion = models.CharField(max_length=100)
    dividendo_por_accion = models.DecimalField(max_digits=14, decimal_places=4, validators=[MinValueValidator(Decimal("0.0001"))])
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.BORRADOR, db_index=True)
    observaciones = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["-gestion", "numero_resolucion"]
        constraints = [models.UniqueConstraint(fields=["gestion", "numero_resolucion"], name="uq_dividendo_gestion_resolucion")]

    def clean(self):
        super().clean()
        if self.fecha_aprobacion and self.fecha_aprobacion < self.fecha_corte:
            raise ValidationError({"fecha_aprobacion": "La fecha de aprobación no puede preceder a la fecha de corte."})
        if self.estado == self.Estado.APROBADO and not self.fecha_aprobacion:
            raise ValidationError({"fecha_aprobacion": "Un dividendo aprobado debe tener fecha de aprobación."})

    def __str__(self):
        return f"Dividendo {self.gestion} - {self.numero_resolucion}"


class LiquidacionDividendo(BaseModel):
    declaracion = models.ForeignKey(DeclaracionDividendo, on_delete=models.PROTECT, related_name="liquidaciones")
    accionista = models.ForeignKey(Accionista, on_delete=models.PROTECT, related_name="liquidaciones_dividendo")
    acciones_elegibles = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    dividendo_bruto = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    retencion = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0.00"))])
    dividendo_neto = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    observaciones = models.TextField(blank=True, default="")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["declaracion", "accionista"], name="uq_liquidacion_dividendo_accionista")]

    def clean(self):
        super().clean()
        if None in (self.acciones_elegibles, self.dividendo_bruto, self.retencion, self.dividendo_neto) or not self.declaracion_id:
            return

        # Validar cálculo bruto
        esperado_bruto = (Decimal(self.acciones_elegibles) * self.declaracion.dividendo_por_accion).quantize(Decimal("0.01"))
        if self.dividendo_bruto != esperado_bruto:
            raise ValidationError({"dividendo_bruto": f"El bruto debe ser {esperado_bruto} según las acciones elegibles."})

        # Validar retenciones y netos
        if self.retencion > self.dividendo_bruto:
            raise ValidationError({"retencion": "La retención no puede superar el bruto."})
        if self.dividendo_neto != self.dividendo_bruto - self.retencion:
            raise ValidationError({"dividendo_neto": "El neto debe ser bruto menos retención."})

    @property
    def total_pagado(self):
        return self.pagos.filter(anulado=False).aggregate(total=Sum("monto"))["total"] or Decimal("0.00")

    @property
    def saldo_pendiente(self):
        return self.dividendo_neto - self.total_pagado

    def __str__(self):
        return f"Liquidación {self.declaracion} - {self.accionista}"


class PagoDividendo(BaseModel):
    class FormaPago(models.TextChoices):
        TRANSFERENCIA = "TRANSFERENCIA", "Transferencia bancaria"
        CHEQUE = "CHEQUE", "Cheque"
        EFECTIVO = "EFECTIVO", "Efectivo"
        OTRO = "OTRO", "Otro"

    liquidacion = models.ForeignKey(LiquidacionDividendo, on_delete=models.PROTECT, related_name="pagos")
    fecha_pago = models.DateField(default=timezone.localdate)
    monto = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    forma_pago = models.CharField(max_length=20, choices=FormaPago.choices)
    referencia_pago = models.CharField(max_length=100, blank=True, default="")
    anulado = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True, default="")

    def clean(self):
        super().clean()
        if self.monto is None or not self.liquidacion_id or self.anulado:
            return

        pagos_previos = self.liquidacion.pagos.filter(anulado=False).exclude(pk=self.pk).aggregate(total=Sum("monto"))["total"] or Decimal("0.00")
        if pagos_previos + self.monto > self.liquidacion.dividendo_neto:
            raise ValidationError({"monto": "El pago supera el saldo pendiente del dividendo."})


class CertificadoAccionario(BaseModel):
    class Estado(models.TextChoices):
        VIGENTE = "VIGENTE", "Vigente"
        ANULADO = "ANULADO", "Anulado"
        REEMPLAZADO = "REEMPLAZADO", "Reemplazado"

    numero = models.CharField(max_length=30, unique=True)
    accionista = models.ForeignKey(Accionista, on_delete=models.PROTECT, related_name="certificados_accionarios")
    tipo_accion = models.ForeignKey(TipoAccion, on_delete=models.PROTECT, related_name="certificados")
    cantidad_certificada = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    fecha_emision = models.DateField(default=timezone.localdate)
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.VIGENTE)
    nombre_titular_snapshot = models.CharField(max_length=250)
    documento_titular_snapshot = models.CharField(max_length=50, blank=True, default="")
    observaciones = models.TextField(blank=True, default="")


class CertificadoDividendo(BaseModel):
    class Estado(models.TextChoices):
        EMITIDO = "EMITIDO", "Emitido"
        ANULADO = "ANULADO", "Anulado"
        REEMPLAZADO = "REEMPLAZADO", "Reemplazado"

    numero = models.CharField(max_length=30, unique=True)
    liquidacion = models.ForeignKey(LiquidacionDividendo, on_delete=models.PROTECT, related_name="certificados")
    fecha_emision = models.DateField(default=timezone.localdate)
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.EMITIDO)
    titular_snapshot = models.CharField(max_length=250)
    importe_neto_snapshot = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    observaciones = models.TextField(blank=True, default="")


def calcular_porcentaje(acciones_accionista, total_acciones):
    if total_acciones <= 0:
        return Decimal("0.00")
    return (Decimal(acciones_accionista) * Decimal("100") / Decimal(total_acciones)).quantize(Decimal("0.01"))