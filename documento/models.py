from django.db import models
from core.models import BaseModel

# Create your models here.
class Documento(BaseModel):
    
    class TipoDocumento(models.IntegerChoices):
        CARTA = 1, "Carta"
        MEMO = 2, "Memo"
        FACTURA = 3, "Factura"
        NOTA = 4, "Nota"
        RESOLUCION = 5, "Resolución"
        DECRETO = 6, "Decreto"
        CERTIFICADO = 7, "Certificado"
        COMPROBANTE = 8, "Comprobante"
        REQUERIMIENTO = 9, "Requerimiento"
        CI = 10, "Carnet de identidad"
        PASAPORTE = 11, "Pasaporte"
        LICENCIA_CONDUCIR = 12, "Licencia de conducir"
        TITULO_BACHILLER = 13, "Titulo de Bachiller"
        CV = 14, "Curriculum Vitae"
        EXAMEN_PREOCUPACIONAL = 15, "Examen preocupacional"
        CERTIFICADO_EXAMEN_MEDICO = 16, "Certificado de examen médico"
        CONTRATO = 17, "Contrato"
        AVISO_AFILIACION = 18, "Aviso de afiliación CPS"
        GESTORA = 19, "Tramite en la gestora"
        BAJA = 20, "Baja médica"
        FICHA_MEDICA = 21, "Ficha médica"
        EVALUACION = 22, "Evaluación"

    tipo_de_documento = models.PositiveSmallIntegerField(choices=TipoDocumento.choices)
    numero = models.CharField(max_length=50, blank=True, null=True)
    fecha_emision = models.DateField(blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    vigente = models.BooleanField(default=True)
    foto = models.ImageField(upload_to="documento/fotos/", blank=True, null=True)
    pdf = models.FileField( upload_to="documento/pdf/", blank=True, null=True)
    url = models.URLField( blank=True, null=True)

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return self.get_tipo_de_documento_display()
