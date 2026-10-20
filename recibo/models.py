# Create your models here.
from django.db import models
from core.models import BaseModel

class DiccionarioRecibo(BaseModel):

    class TipoRecibo(models.IntegerChoices):
        INGRO = 1, "Recibo de Ingro"
        PAGO = 2, "Recibo de Pago"
        ORDEN_PAGO = 3, "Orden de Pago"
    

    class TipoPago(models.IntegerChoices):
        VIATICOS = 1, "Viáticos"
        SERVICIOS = 2, "Servicios"
        COMPRAS = 3, "Compras"
        JORNAL = 4, "Jornal"
        SIN_IMPUESTOS = 5, "Sin Impuestos"

    tipo_recibo = models.PositiveSmallIntegerField(choices=TipoRecibo.choices)
    codigo = models.PositiveIntegerField()
    nombre = models.CharField(max_length=150)
    concepto = models.TextField(blank=True,default="")
    proyecto = models.CharField(max_length=150, blank=True, default="")
    imputacion_contable = models.CharField(max_length=100,blank=True,default="")
    centro_costo = models.CharField(max_length=100,blank=True,default="")
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["tipo_recibo", "nombre"]
        constraints = [models.UniqueConstraint(fields=["tipo_recibo", "codigo"],name="unique_diccionario_tipo_codigo")]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Recibo(BaseModel):

    class Lugar(models.IntegerChoices):
        COCHABAMBA = 1, "Cochabamba"
        LA_PAZ = 2, "La Paz"
        SUCRE = 3, "Sucre"
        SANTA_CRUZ = 4, "Santa Cruz"
        ORURO = 5, "Oruro"
        POTOSI = 6, "Potosí"
        TARIJA = 7, "Tarija"
        TRINIDAD = 8, "Trinidad"
        COBIJA = 9, "Cobija"
        BUENOS_AIRES = 10, "Buenos Aires"
        SANTIAGO = 11, "Santiago"
        LIMA = 12, "Lima"
        SAO_PAULO = 13, "São Paulo"
        RIO_DE_JANEIRO = 14, "Río de Janeiro"
        BOGOTA = 15, "Bogotá"
        ASUNCION = 16, "Asunción"
        MONTEVIDEO = 17, "Montevideo"
        QUITO = 18, "Quito"
        CARACAS = 19, "Caracas"
        MIAMI = 20, "Miami"
        NEW_YORK = 21, "New York"
        MADRID = 22, "Madrid"
        BARCELONA = 23, "Barcelona"
        PARIS = 24, "París"
        LONDREs = 25, "Londres"
        AUSTRIA = 26, "Austria"
        AUSTRALIA = 27, "Australia"
        ALEMANIA = 28, "Alemania"
        HOLANDA = 29, "Holanda"

    class FormaPago(models.IntegerChoices):
        EFECTIVO = 1, "Efectivo"
        TRANSFERENCIA = 2, "Transferencia"
        CHEQUE = 3, "Cheque"
        DEPOSITO = 4, "Depósito"


    class Banco(models.IntegerChoices):
        BNB = 1, "BNB"
        BANCOMUNIDAD = 2, "Bancomunidad"

    CUENTAS_BANCOS = {
        Banco.BNB: "300 - 0093083",
        Banco.BANCOMUNIDAD: "3040 - 001276",
    }

    class Moneda(models.IntegerChoices):
        BS = 1, "Bs."
        USD = 2, "USD"

    #id automatico
    empleado_registra = models.ForeignKey("empleado.Empleado", on_delete=models.CASCADE, blank=True, null=True)
    tipo_recibo = models.PositiveSmallIntegerField(choices=DiccionarioRecibo.TipoRecibo.choices) 
    empleado_emitidor = models.CharField(max_length=3) #ver si se necita fk con conector a empleado son inicial, tambien para poner en recibo
    num = models.IntegerField()
    beneficiario = models.CharField(max_length=200) #puede conectar a  nombr de empleados, nombr de client de otro modulo, no obligatorio puto q se puede cribir de otros pero  importante que aparezca la concexion para un autocompletado
    monto = models.DecimalField(max_digits=15,decimal_places=2)
    concepto = models.TextField()
    forma_pago = models.PositiveSmallIntegerField(choices=FormaPago.choices)
    numero_cheque = models.CharField(max_length=50)
    banco_deposito = models.PositiveSmallIntegerField(choices=Banco.choices)
    num_cuenta_deposito = models.CharField(max_length=50, blank=True, default="")
    lugar = models.PositiveSmallIntegerField(choices=Lugar.choices)
    fecha_emision = models.DateField()#obligatorio puto q se puede poner de dia anterior o etc
    tipo_pago = models.PositiveSmallIntegerField(choices=DiccionarioRecibo.TipoPago.choices, null=True, blank=True)
    costo_total = models.DecimalField(max_digits=15,decimal_places=2)
    imputacion_contable = models.CharField(max_length=50, blank=True, default="")
    centro_costo = models.CharField(max_length=50, blank=True, default="")
    proyecto = models.CharField(max_length=50, blank=True, default="")
    responsable_inicial = models.CharField(max_length=4) #ver si se necita fk con conector a empleado son inicial, tambien para poner en recibo
    activo = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

class Viaticos(BaseModel):
    #id automatico
    beneficiario = models.ForeignKey("persona.Persona", on_delete=models.CASCADE, blank=True, null=True)
    dia_turno = models.DecimalField(max_digits=15,decimal_places=2)
    transporte = models.DecimalField(max_digits=15,decimal_places=2)
    alimentacion = models.DecimalField(max_digits=15,decimal_places=2)
    costo_dias_total = models.DecimalField(max_digits=15,decimal_places=2)
    costo_transporte_noct = models.DecimalField(max_digits=15,decimal_places=2)
    costo_transporte_galpon = models.DecimalField(max_digits=15,decimal_places=2)
    costo_transporte_cumbre = models.DecimalField(max_digits=15,decimal_places=2)
    costo_total = models.DecimalField(max_digits=15,decimal_places=2)