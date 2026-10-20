# Create your models here.
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from core.models import BaseModel

class CategoriaCentral(BaseModel):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Categoría central"
        verbose_name_plural = "Categorías central"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Subcategoria(BaseModel):
    categoria = models.ForeignKey(CategoriaCentral, on_delete=models.PROTECT, related_name="subcategoria")
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Subcategoría"
        verbose_name_plural = "Subcategorías"
        ordering = ["categoria__nombre", "nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["categoria", "nombre"],
                name="unique_subcategoria_por_categoria"
            )
        ]

    def __str__(self):
        return f"{self.categoria.nombre} → {self.nombre}"

class UbicacionArchivo(BaseModel):
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Ubicación de archivo"
        verbose_name_plural = "Ubicacion de archivo"
        ordering = ["nombre"]
        
    def __str__(self):
        return self.nombre

class Mensajeria(BaseModel):
    nombre = models.CharField(max_length=100, unique=True)
    contacto = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    activo = models.BooleanField(default=True)
    class Meta:
        verbose_name = "Empresa de mensajería"
        verbose_name_plural = "Empresas de mensajería"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class SeguimientoCopiaSellada(BaseModel):
    correspondencia = models.ForeignKey("correspondencia.Correspondencia", on_delete=models.CASCADE, related_name="seguimiento_copia_sellada",)
    mensajeria = models.ForeignKey(Mensajeria, on_delete=models.PROTECT, related_name="envio", null=True, blank=True,)
    enviado_por = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT, related_name="copia_sellada_enviada", null=True, blank=True,)
    copia_sellada = models.BooleanField(default=False)
    fecha_enviado = models.DateField(null=True, blank=True)
    numero_guia = models.CharField(max_length=30, blank=True)
    fecha_que_trae = models.DateField(null=True, blank=True)
    observacion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Seguimiento de copia sellada"
        verbose_name_plural = "Seguimientos de copias selladas"
        ordering = ["-fecha_enviado", "-id"]

    def __str__(self):
        return f"Copia sellada de {self.correspondencia_id}"


class EventoSeguimiento(BaseModel):
    class TipoEvento(models.TextChoices):
        REGISTRO = "REGISTRO", "Registro"
        ENVIO = "ENVIO", "Envío"
        LLAMADA = "LLAMADA", "Llamada"
        CORREO = "CORREO", "Correo electrónico"
        RECLAMO = "RECLAMO", "Reclamo"
        COMPROMISO = "COMPROMISO", "Compromiso de respuesta"
        RECEPCION = "RECEPCION", "Recepción de respuesta"
        ENTREGA = "ENTREGA", "Entrega física"
        OTRO = "OTRO", "Otro"

    # En SeguimientoCopiaSellada:
    correspondencia = models.ForeignKey("correspondencia.correspondencia", on_delete=models.CASCADE, related_name="evento_seguimiento",)
    tipo_evento = models.CharField( max_length=20, choices=TipoEvento.choices,)
    fecha_evento = models.DateTimeField(default=timezone.now)
    realizado_por = models.ForeignKey("empleado.Empleado", on_delete=models.PROTECT, related_name="evento_correspondencia", null=True, blank=True,)
    contacto = models.CharField(max_length=150, blank=True)
    resultado = models.TextField(blank=True)
    proxima_fecha = models.DateField(null=True, blank=True)
    observacion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Evento de seguimiento"
        verbose_name_plural = "Eventos de seguimiento"
        ordering = ["-fecha_evento", "-id"]

    def __str__(self):
        return (
            f"{self.correspondencia.num_registro} - "
            f"{self.get_tipo_evento_display()} - "
            f"{self.fecha_evento:%d/%m/%Y}"
        )

class correspondencia(BaseModel):

    class TipoReferencia (models.TextChoices):
        SY = "SY", "SY - Documento enviado"
        MEMO = "ME", "Memorándum"
        FACTURA = "FT", "Factura"
        RESOLUCION = "RE", "Resolución"
        DECRETO = "DR", "Decreto"
        CERTIFICADO = "CR", "Certificado"
        COMPROBANTE = "CM", "Comprobante"
        REQUERIMIENTO = "RQ", "Requerimiento"
    
    class TipoEntrega(models.IntegerChoices):
        DESPACHADO = 1, "Despachado"
        FISICO = 2, "Fisico"

    class Estado(models.IntegerChoices):
        CERRADO = 1, "Cerrado"
        PENDIENTE = 2, "Pendiente"

    class Recepcion_Despacho(models.IntegerChoices):
        FISICO = 1, "Físico"
        Despacho = 2, "Despacho"

    class Adjunto(models.IntegerChoices):
        CD = 1, "CD"
        PENDRIVE = 2, "Pendrive"
        LIBRO = 3, "Libro"
        CV = 4, "Curriculum Vitae"
        COMPROBANTE = 5, "Comprobante"
        COPIA_CI = 6, "Copia del CI"
        COPIA_PASAPORTE = 7, "Copia del Pasaporte"
        COPIA_TITULO_UNIVERSITARIO = 8, "Copia de Titulo Universitario"
        COPIA_CERTIFICADO = 9, "Copia de Certificado"
        COPIA_FACTURA = 10, "Copia de Factura"
        COPIA_CONTRATO = 11, "Copia de contrato"
        COPIA_ESTADO_CUENTA = 12, "Copia de estado de Cuenta"
        COPIA_CERTIFICADO_MEDICO = 13, "Copia de Certificado Médico"
        COPIA_CARTA_RECOMENDACION = 14, "Copia de Carta de Recomendación"
        COPIA_TRAMITE = 15, "Copia de Trámite"
        LLAVERO = 16, "Llavero"
        CALENDARIO = 17, "Calendario"
        PERIODICO = 18, "Periódico"
        OBSEQUIO = 19, "Obsequio"

    #id automatico
    fecha_sellado = models.DateTimeField(auto_now_add=True)
    fecha_entrega_digital = models.DateTimeField(null=True,blank=True,verbose_name="Fecha y hora de entrega digital",) 
    fecha_entrega_fisica = models.DateTimeField(null=True,blank=True,verbose_name="Fecha y hora de entrega física",)
    tipo_entrega = models.IntegerField(choices=TipoEntrega.choices)
    tipo_documento =  models.ForeignKey("documento.Documento", on_delete=models.PROTECT, related_name="correspondencia")
    tipo_referencia = models.CharField(max_length=2,choices=TipoReferencia.choices,blank=True,default="",verbose_name="Tipo de referencia",)
    num_ref = models.CharField(max_length=50,blank=True,default="",db_index=True,verbose_name="Número de referencia",help_text="Ej.: SY-450, ME-18, F-320/2026, D-52/2026")
    destinatario_remitente = models.CharField(max_length=150) #deberia poder aparecer sugerencias si ya hay similar por ejemplo ing. Julio Arancibia y ni bien criba Ing. Julio ara me salte o por arancibia o no se si frontend o backend
    empresa = models.ForeignKey("institucion.Institucion", on_delete=models.PROTECT, related_name="correspondencia") #ver institucion creadas con id modelo aparte
    asunto = models.CharField(max_length=200)
    num_registro = models.PositiveIntegerField()
    num_hoja = models.PositiveSmallIntegerField()
    entregado_a = models.ManyToManyField("empleado.Empleado", related_name="Entregado_a", blank=True) #actually this must be a one to many but this is to similar at be wanna 
    revisado_por = models.ManyToManyField("empleado.Empleado", related_name="Revisado_por", blank=True) #actually this must be a one to many but this is to similar at be wanna 
    responsable = models.ManyToManyField("empleado.Empleado", related_name="Responsable", blank=True) #actually this must be a one to many but this is to similar at be wanna 
    categoria_central = models.ForeignKey("correspondencia.CategoriaCentral",on_delete=models.PROTECT,related_name="correspondencia",)
    subcategoria = models.ForeignKey("correspondencia.Subcategoria",on_delete=models.PROTECT,related_name="correspondencia",)
    archivado_en = models.ForeignKey("correspondencia.UbicacionArchivo",on_delete=models.PROTECT,related_name="correspondencia",)
    estado = models.PositiveSmallIntegerField(choices=Estado.choices, default=Estado.CERRADO)
    plazo_respuesta = models.DateField(blank=True, null=True)
    recepcion_Despacho = models.PositiveSmallIntegerField(choices=Recepcion_Despacho.choices)
    quien_pera_respuesta = models.CharField(max_length=150, blank=True)
    archivo_link =models.URLField(blank=True, null=True) #puede estar con modulo documentos
    foto = models.ImageField(upload_to="correspondencia/", blank=True, null=True) #puede estar con modulo documentos
    adjunto = models.PositiveSmallIntegerField(choices=Adjunto.choices, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    carta_respuesta = models.ForeignKey("self", on_delete=models.SET_NULL, related_name="respuesta",blank=True, null=True)
    fecha_guia = models.CharField(max_length=30)
    def __str__(self):
        return f"{self.num_registro} - {self.asunto}"

    def clean(self):
        super().clean()

        if self.categoria_central_id and self.subcategoria_id:
            if (
                self.subcategoria.categoria_id
                != self.categoria_central_id
            ):
                raise ValidationError({
                    "subcategoria": (
                        "La subcategoría seleccionada no pertenece "
                        "a la categoría central elegida."
                    )
                })