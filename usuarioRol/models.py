from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from core.models import BaseModel
#Mantener 20 años de un usuarioRol con softdelete contratos, finiquitos, desvinculaciones y hojas de calculo de beneficios//planillas de sueldos, boletas de pago y registros de asistencia 5 años//documentacion de respaldos impositivos 8 años//#aportes a la seguridad social minimo 10 años//#los cvs y procesos de seleccion se conservan maximo 3 años //#al cumplirse los 5 años de la baja del empleado, traslada sus datos operativos a una base de datos histórica inmutable, cifrada y desconectada del software de uso diario de Recursos Humanos, conservando únicamente el acceso para el equipo Legal ante eventuales demandas de orden constitucional
#USUARIO y base de auditoria y control
class UsuarioManager(BaseUserManager):
    """
    Manager personalizado para manejar la creación de usuarios usando el correo electrónico
    como identificador principal en lugar de username.
    """
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError("El correo electrónico es obligatorio.")
        correo = self.normalize_email(correo)
        # No permitir que se cree una cuenta sin contraseña inicial, //# mediante este método. Para invitaciones, se puede usar //# un flujo separado de activación y establecimiento de clave.
        if not password:
            raise ValueError("Debes proporcionar una contraseña inicial.")
        
        # Asignamos el correo al username por defecto para evitar problemas con AbstractUser
        extra_fields.setdefault('username', correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault(
            "estado_cuenta",
            Usuario.EstadoCuenta.ACTIVA,
        )

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "El superusuario debe tener is_superuser=True."
            )

        if extra_fields.get("estado_cuenta") != Usuario.EstadoCuenta.ACTIVA:
            raise ValueError("El superusuario debe tener cuenta activa.")

        return self.create_user(correo, password, **extra_fields)


class MetodoAutenticacion(BaseModel):
    #id automatico
    codigo = models.CharField(max_length=50,unique=True)
    nombre = models.CharField(max_length=128)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser, BaseModel):
    
    class EstadoCuenta(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        ACTIVA = "ACTIVA", "Activa"
        BLOQUEADA = "BLOQUEADA", "Bloqueada"
        SUSPENDIDA = "SUSPENDIDA", "Suspendida"
        INACTIVA = "INACTIVA", "Inactiva"

    # AbstractUser ya tiene username, email, password y last_login.
    #Crea el id automaticamente en la base de datos
    correo = models.EmailField(unique=True, max_length=254)
    # el password ya viene por defecto en el abstractuser >>password = models.CharField (max_length=128)
    estado_cuenta = models.CharField(max_length=20, choices=EstadoCuenta.choices, default=EstadoCuenta.PENDIENTE)
    #abstractuser ya tiene last_login ultimo_login = models.DateTimeField(null=True, blank=True)
    requiere_cambio_password = models.BooleanField(default=True)

    # Metadatos de seguridad.
    fecha_activacion = models.DateTimeField(null=True,blank=True,)
    fecha_ultimo_cambio_password = models.DateTimeField(null=True,blank=True, )
    intentos_fallidos = models.PositiveSmallIntegerField(default=0)
    bloqueado_hasta = models.DateTimeField(null=True,blank=True,)

    # Configuración de autenticación por correo
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UsuarioManager()
    def __str__(self):
        return self.correo

    def clean(self):
        super().clean()

        # Mantener coherentes el estado de cuenta y el acceso
        # a la autenticación de Django.
        if (
            self.estado_cuenta != self.EstadoCuenta.ACTIVA
            and self.is_active
        ):
            raise ValidationError({
                "is_active": (
                    "La cuenta debe estar activa para permitir "
                    "el acceso."
                )
            })

    def save(self, *args, **kwargs):
        # Protección adicional para no activar accidentalmente
        # una cuenta pendiente, bloqueada, suspendida o inactiva.
        if self.estado_cuenta != self.EstadoCuenta.ACTIVA:
            self.is_active = False

        super().save(*args, **kwargs)


class UsuarioMetodo(BaseModel):
    #id automatico
    #usuario
    #metodo
    usuario = models.ForeignKey("usuarioRol.Usuario", on_delete=models.CASCADE, related_name = "metodo_autenticacion")
    metodo = models.ForeignKey("usuarioRol.MetodoAutenticacion", on_delete=models.PROTECT, related_name= "usuarios_metodo")
    activo = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(null=True, blank=True)
    ultima_verificacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        # Evita duplicar el mismo método para un usuario.
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "metodo"],
                name="uq_usuario_metodo",
            )
        ]

class Rol(BaseModel):
    #id automatico
    nombre = models.CharField(max_length=128, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class UsuarioRol(BaseModel):
    #id automatico
    #id de usuario
    #id de rol
    usuario = models.ForeignKey("usuarioRol.Usuario", on_delete=models.CASCADE, related_name="rol_asignado")
    rol = models.ForeignKey("usuarioRol.Rol", on_delete=models.PROTECT, related_name="usuario_rol")
    fecha_asignacion = models.DateTimeField(default=timezone.now) #no puede ser auto add porque subire historial, talvez para practicidad
    activo = models.BooleanField(default=True)

    class Meta:
        constraints = [
            #un usuario no necesita el mismo rol asignado dos vec.
            models.UniqueConstraint(
                fields=["usuario", "rol"],
                name="uq_usuario_rol"
            )
        ]

class Modulo(BaseModel):
    #id automatico
    nombre = models.CharField(max_length=128)
    descripcion = models.TextField()
    icono = models.CharField(max_length=100,blank=True)
    orden = models.PositiveIntegerField(default=0) #sirve para mover en el frontend y que se guarde
    activo = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
    
class Accion(BaseModel):
    #id automatico
    nombre = models.CharField(max_length=128, unique= True)
    descripcion = models.TextField()
    activo = models.BooleanField(default=False)

    def __str__(self):
            return self.nombre

class Permiso(BaseModel):
    #id automatico
    nombre = models.CharField (max_length=128)
    codigo = models.CharField(max_length=128, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    #id de modulo
    #id de accion
    modulo = models.ForeignKey("usuarioRol.Modulo", on_delete = models.PROTECT, related_name="permiso_modulo")
    accion = models.ForeignKey("usuarioRol.Accion", on_delete = models.PROTECT, related_name="permiso_accion")

    class Meta:
        constraints = [
            #Cada combinación módulo-acción debe ser única.
            models.UniqueConstraint(
                fields=["modulo", "accion"],
                name="uq_modulo_accion",
            )
        ]

class RolPermiso (BaseModel):
    #id automatico
    #id rol
    #id permiso
    rol = models.ForeignKey("usuarioRol.Rol", on_delete = models.PROTECT, related_name = "permiso_asignado")
    permiso = models.ForeignKey("usuarioRol.Permiso", on_delete = models.PROTECT, related_name="rol_permiso")
    activo = models.BooleanField(default=True)

    class Meta:
        constraints = [
            #Cada combinación módulo-acción debe ser única.
            models.UniqueConstraint(
                fields=["rol", "permiso"],
                name="uq_rol_permiso",
            )
        ]