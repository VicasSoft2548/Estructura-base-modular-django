from django.db import models
from core.models import BaseModel

# Create your models here.
class IntentoLogin(BaseModel):

    class ResultadoLogin(models.TextChoices):
        EXITOSO = "EXITOSO", "Exitoso"
        FALLIDO = "FALLIDO", "Fallido"
        BLOQUEADO = "BLOQUEADO", "Bloqueado"
        MFA_REQUERIDO = "MFA_REQUERIDO", "Mfa_Requerido"
        MFA_FALLIDO = "MFA_FALLIDO", "Mfa_fallido"
    #id automatico
    usuario = models.ForeignKey("usuarioRol.Usuario", on_delete=models.SET_NULL, blank=True, null=True)
    dispositivo = models.ForeignKey("auditoria.Dispositivo", on_delete=models.SET_NULL, blank=True, null=True)
    usuario_metodo = models.ForeignKey("usuarioRol.UsuarioMetodo", on_delete=models.SET_NULL, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True, db_index=True)
    ip = models.GenericIPAddressField(null=True, blank=True, db_index=True)
    user_agent = models.TextField(blank=True)
    resultado = models.CharField(max_length=20, choices=ResultadoLogin.choices, db_index=True) #fallo o no
    motivo = models.TextField(blank=True) #si acaso falla poner porque

class Dispositivo(BaseModel):
    class TipoDispositivo(models.TextChoices):
        PC = "PC", "Computadora"
        MOVIL = "MOVIL", "Móvil"
        TABLET = "TABLET", "Tablet"
        OTRO = "OTRO", "Otro" 

    #id automatico
    usuario = models.ForeignKey("usuarioRol.Usuario", on_delete=models.CASCADE, null=True)
    identificador = models.CharField(max_length=255, db_index=True)
    tipo = models.CharField(max_length=20, choices=TipoDispositivo.choices) #Tipo_dispositivo
    sistema_operativo = models.CharField(max_length=100, blank=True)
    navegador = models.CharField(max_length=100, blank=True)
    aplicacion = models.CharField(max_length=100, blank=True)
    nombre_dispositivo =  models.CharField(max_length=150, blank=True)
    ip_ultimo_acceso = models.GenericIPAddressField(null=True, blank=True)
    fecha_primer_acceso = models.DateTimeField(auto_now_add=True)
    fecha_ultimo_acceso = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)

class Sesion(BaseModel):
    class EstadoSesion(models.TextChoices):
        ACTIVA = "ACTIVA", "Activa"
        CERRADA = "CERRADA", "Cerrada"
        EXPIRADA = "EXPIRADA", "Expirada"
        REVOCADA = "REVOCADA", "Revocada"

    #id automatico
    usuario = models.ForeignKey("usuarioRol.Usuario", on_delete=models.CASCADE, blank = False, null = True)
    dispositivo = models.ForeignKey("auditoria.Dispositivo", on_delete=models.CASCADE, blank=False, null= True)
    usuario_metodo = models.ForeignKey("usuarioRol.UsuarioMetodo", on_delete=models.CASCADE, blank=False, null= True)
    fecha_inicio = models.DateTimeField(db_index=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    ultima_actividad = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=EstadoSesion.choices, default=EstadoSesion.ACTIVA, db_index=True)
    identificador_hash = models.CharField(max_length=128,unique=True)
    ip_inicio = models.GenericIPAddressField(null=True,blank=True)
    ip_fin = models.GenericIPAddressField(null=True,blank=True)
    user_agent = models.TextField(blank=True)

class Auditoria(BaseModel):
    class ResultadoAuditoria(models.TextChoices):
        EXITOSO = "EXITOSO", "Exitoso"
        FALLIDO = "FALLIDO", "Fallido"
        RECHAZADO = "RECHAZADO", "Rechazado"

    #id automatico
    sesion = models.ForeignKey("Sesion", on_delete=models.SET_NULL, null = True)
    modulo = models.ForeignKey("usuarioRol.Modulo", on_delete=models.SET_NULL,null = True)
    accion = models.ForeignKey("usuarioRol.Accion", on_delete=models.SET_NULL,null = True)
    recurso = models.CharField(max_length=100) #Sobre que realizó la acción
    resultado = models.CharField(max_length=20, choices=ResultadoAuditoria.choices, db_index=True) #El resultado de la operación que se efectuó
    fecha_hora = models.DateTimeField(auto_now_add=True, db_index=True)  #cuando se ejecutó la acción
    ip = models.GenericIPAddressField(db_index=True)
    user_agent = models.TextField() #agente que uso, por ej mozzilla, chrome, brave
    descripcion = models.TextField()

class Auditoria_detalle(BaseModel):
    #id automatico
    auditoria= models.ForeignKey("auditoria.Auditoria", on_delete=models.CASCADE, blank=False, null = True)
    campo = models.CharField(max_length=100, db_index=True) #correo, estado_cuenta, nombre, descripcion, activo
    valor_anterior = models.TextField(null=True, blank=True)
    valor_nuevo = models.TextField(null=True, blank=True)
