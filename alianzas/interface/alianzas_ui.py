# alliances/alianzas_ui.py
from __future__ import annotations

from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user

from app.models import Negocio  # ajusta si tu import real es distinto

alianzas_ui_bp = Blueprint("alianzas_ui", __name__, url_prefix="/alianzas")


def get_negocio_actual():
    """
    Obtiene el negocio principal del usuario.
    Ajusta si tu relación usuario↔negocio difiere.
    """
    # Caso 1: relación 1–1
    if hasattr(current_user, "negocio") and current_user.negocio:
        return current_user.negocio
    # Caso 2: relación 1–N
    if hasattr(current_user, "negocios") and current_user.negocios:
        return current_user.negocios[0]
    # Fallback
    return Negocio.query.filter_by(usuario_id=current_user.id).first()


@alianzas_ui_bp.route("", methods=["GET"])
@alianzas_ui_bp.route("/", methods=["GET"])
@login_required
def manage_alliances():
    negocio = get_negocio_actual()
    if not negocio:
        flash("Primero debe crear un negocio.", "danger")
        return redirect(url_for("negocios.crear"))
    # La UI consumirá el gateway interno /alliances-api via fetch
    return render_template("slider/manage_alliances.html", negocio=negocio)


# ======= NUEVO: catálogo de negocios en JSON =======
@alianzas_ui_bp.route("/negocios-json", methods=["GET"])
@login_required
def negocios_json():
    """
    Devuelve negocios en formato JSON para poblar selects/autocomplete.

    Query params:
      - q: filtro por nombre (ILIKE %q%)
      - exclude_me: "1"/"true" para excluir mi propio negocio (default: 1)
      - limit: límite de filas (default: 200)
    """
    q = (request.args.get("q") or "").strip()
    exclude_me = (request.args.get("exclude_me", "1").lower() in ("1", "true", "yes"))
    limit = request.args.get("limit", type=int) or 200

    my = get_negocio_actual()

    query = Negocio.query
    if exclude_me and my:
        query = query.filter(Negocio.id != my.id)
    if q:
        query = query.filter(Negocio.nombre.ilike(f"%{q}%"))

    rows = query.order_by(Negocio.nombre.asc()).limit(limit).all()
    payload = [
        {
            "id": n.id,
            "nombre": n.nombre,
            "ruc": n.ruc,
            "razon_social": n.razon_social,
        }
        for n in rows
    ]
    return jsonify(payload), 200
