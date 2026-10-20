# usuarioRol/services.py

from django.core.exceptions import ValidationError
from django.db import transaction

from auditoria.models import Auditoria, Auditoria_detalle
from usuarioRol.models import Usuario


@transaction.atomic
def cambiar_correo(
    *,
    actor,
    usuario,
    correo_nuevo,
    sesion,
    modulo,
    accion,
    ip,
    user_agent,
):
    # Bloquear las filas durante la operación.
    usuario = Usuario.objects.select_for_update().get(
        pk=usuario.pk
    )

    if usuario.deleted_at is not None:
        raise ValidationError(
            "No se puede modificar un usuario desactivado."
        )

    if not actor.is_active:
        raise ValidationError(
            "El actor está desactivado."
        )

    if sesion.usuario_id != actor.pk:
        raise ValidationError(
            "La sesión no pertenece al actor."
        )

    if sesion.estado != "ACTIVA":
        raise ValidationError(
            "La sesión no está activa."
        )

    # Aquí debes verificar que el actor tenga permiso
    # para cambiar el correo del usuario indicado.

    correo_anterior = usuario.correo

    if correo_anterior == correo_nuevo:
        return usuario

    usuario.correo = correo_nuevo
    usuario.save(update_fields=["correo", "updated_at"])

    evento = Auditoria.objects.create(
        sesion=sesion,
        modulo=modulo,
        accion=accion,
        recurso="Usuario",
        resultado="EXITOSO",
        ip=ip,
        user_agent=user_agent,
        descripcion="Cambio de correo de usuario.",
    )

    Auditoria_detalle.objects.create(
        auditoria=evento,
        campo="correo",
        valor_anterior=correo_anterior,
        valor_nuevo=correo_nuevo,
    )

    return usuario
