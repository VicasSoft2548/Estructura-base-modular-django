from django.shortcuts import render

# Create your views here.

from django.http import JsonRponse
from django.db.models import Q
from django.views.decorators.http import require_GET

from .models import correspondencia


@require_GET
def sugerir_destinatarios(requt):
    termino = requt.GET.get("q", "").strip()

    if len(termino) < 2:
        return JsonRponse({"resultados": []})

    coincidencias = (
        correspondencia.objects
        .filter(
            Q(destinatario_remitente__icontains=termino)
        )
        .valu_list("destinatario_remitente", flat=True)
        .distinct()
        .order_by("destinatario_remitente")[:10]
    )

    return JsonRponse({
        "resultados": list(coincidencias)
    })#################revisar a detalle 