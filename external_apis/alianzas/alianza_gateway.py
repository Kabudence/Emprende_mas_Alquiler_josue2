# external_apis/alianzas/alianza_gateway.py
from __future__ import annotations
from flask import Blueprint, request, jsonify
from datetime import datetime

# Cliente del microservicio de alianzas (debes implementarlo de forma análoga a coupons_client)
from external_apis.alianzas import alianza_client as ac

alianza_gateway_bp = Blueprint("alianza_gateway", __name__, url_prefix="/alliances-api")

# -------- Helpers --------
def _as_iso(dt) -> str | None:
    if not dt:
        return None
    if isinstance(dt, datetime):
        return dt.isoformat()
    return str(dt)

def _from_client(resp_tuple):
    status, body = resp_tuple
    return jsonify(body), status


# ========== SOLICITUD / CRUD LÓGICO ==========

@alianza_gateway_bp.route("/alliances", methods=["POST"])
def gw_solicitar_alianza():
    """
    Body JSON:
    {
      "solicitante_negocio_id": 1,
      "receptor_negocio_id": 2,
      "motivo": "opcional"
    }
    """
    data = request.get_json(silent=True) or {}
    return _from_client(ac.solicitar_alianza(
        solicitante_negocio_id = int(data.get("solicitante_negocio_id")),
        receptor_negocio_id    = int(data.get("receptor_negocio_id")),
        motivo                 = data.get("motivo"),
    ))


@alianza_gateway_bp.route("/alliances", methods=["GET"])
def gw_listar_alianzas():
    """
    Query params opcionales:
      ?negocio_id=123
      ?estado=PENDIENTE|ACEPTADA|RECHAZADA|CANCELADA|SUSPENDIDA
    """
    negocio_id = request.args.get("negocio_id", type=int)
    estado     = request.args.get("estado", type=str)
    return _from_client(ac.listar_alianzas(negocio_id=negocio_id, estado=estado))


@alianza_gateway_bp.route("/alliances/<int:alianza_id>", methods=["GET"])
def gw_obtener_alianza(alianza_id: int):
    return _from_client(ac.obtener_alianza(alianza_id))


@alianza_gateway_bp.route("/alliances/by-business/<int:negocio_id>", methods=["GET"])
def gw_listar_por_negocio(negocio_id: int):
    return _from_client(ac.listar_por_negocio(negocio_id))


# ========== BANDEJAS / CONSULTAS ÚTILES ==========

@alianza_gateway_bp.route("/alliances/pending/received", methods=["GET"])
def gw_pendientes_recibidas():
    negocio_id = request.args.get("negocio_id", type=int)
    return _from_client(ac.pendientes_recibidas(negocio_id))


@alianza_gateway_bp.route("/alliances/pending/sent", methods=["GET"])
def gw_pendientes_enviadas():
    negocio_id = request.args.get("negocio_id", type=int)
    return _from_client(ac.pendientes_enviadas(negocio_id))


@alianza_gateway_bp.route("/alliances/active", methods=["GET"])
def gw_activas():
    negocio_id = request.args.get("negocio_id", type=int)
    return _from_client(ac.activas(negocio_id))


@alianza_gateway_bp.route("/alliances/exists", methods=["GET"])
def gw_existe_entre():
    negocio_a = request.args.get("negocio_a", type=int)
    negocio_b = request.args.get("negocio_b", type=int)
    return _from_client(ac.existe_entre(negocio_a, negocio_b))


# ========== TRANSICIONES DE ESTADO ==========

def _actor_and_reason():
    data = request.get_json(silent=True) or {}
    actor  = int(data.get("actor_negocio_id"))
    motivo = data.get("motivo")
    return actor, motivo

@alianza_gateway_bp.route("/alliances/<int:alianza_id>/accept", methods=["PUT"])
def gw_aceptar(alianza_id: int):
    actor, motivo = _actor_and_reason()
    return _from_client(ac.aceptar(alianza_id, actor, motivo=motivo))

@alianza_gateway_bp.route("/alliances/<int:alianza_id>/reject", methods=["PUT"])
def gw_rechazar(alianza_id: int):
    actor, motivo = _actor_and_reason()
    return _from_client(ac.rechazar(alianza_id, actor, motivo=motivo))

@alianza_gateway_bp.route("/alliances/<int:alianza_id>/cancel", methods=["PUT"])
def gw_cancelar(alianza_id: int):
    actor, motivo = _actor_and_reason()
    return _from_client(ac.cancelar(alianza_id, actor, motivo=motivo))

@alianza_gateway_bp.route("/alliances/<int:alianza_id>/suspend", methods=["PUT"])
def gw_suspender(alianza_id: int):
    actor, motivo = _actor_and_reason()
    return _from_client(ac.suspender(alianza_id, actor, motivo=motivo))

@alianza_gateway_bp.route("/alliances/<int:alianza_id>/reactivate", methods=["PUT"])
def gw_reactivar(alianza_id: int):
    actor, motivo = _actor_and_reason()
    return _from_client(ac.reactivar(alianza_id, actor, motivo=motivo))
