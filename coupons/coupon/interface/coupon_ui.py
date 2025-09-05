# coupons/coupon/interface/coupon_ui.py
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import (
    Negocio,
    Producto,
    ProductoDetalle,
    Tamanio,
    Color,
    ServicioCompleto,  # NEW: servicios completos
)

coupon_ui_bp = Blueprint("coupon_ui", __name__, url_prefix="/coupons")


def get_negocio():
    return Negocio.query.filter_by(usuario_id=current_user.id).first()


@coupon_ui_bp.route("/", methods=["GET"])
@login_required
def manage_coupons():
    negocio = get_negocio()
    if not negocio:
        flash("Primero debe crear un negocio.", "danger")
        return redirect(url_for("negocios.crear"))
    return render_template("slider/manage_coupons.html", negocio=negocio)


@coupon_ui_bp.route("/products-json", methods=["GET"])
@login_required
def products_json():
    """
    Lista de productos (no variantes) del negocio, para poblar los selectores.
    """
    negocio = get_negocio()
    if not negocio:
        return jsonify([]), 200
    qs = (
        Producto.query
        .filter_by(id_negocio=negocio.id)
        .order_by(Producto.nombre.asc())
        .all()
    )
    data = [{"id": p.id, "name": p.nombre} for p in qs]
    return jsonify(data), 200


@coupon_ui_bp.route("/services-json", methods=["GET"])
@login_required
def services_json():
    """
    Lista de servicios completos del negocio para usar en 'aplicación' o 'triggers'.
    (No hay variantes en servicios).
    """
    negocio = get_negocio()
    if not negocio:
        return jsonify([]), 200
    rows = (
        ServicioCompleto.query
        .filter_by(id_negocio=negocio.id)
        .order_by(ServicioCompleto.titulo_publicacion.asc())
        .all()
    )
    data = [{"id": s.id, "name": s.titulo_publicacion} for s in rows]
    return jsonify(data), 200


@coupon_ui_bp.route("/product-variants-json/<int:product_id>", methods=["GET"])
@login_required
def product_variants_json(product_id: int):
    """
    Variantes (ProductoDetalle) de un producto: retornamos un label bonito para el combo.
    """
    dets = (
        ProductoDetalle.query
        .filter_by(producto_id=product_id)
        .order_by(ProductoDetalle.id.asc())
        .all()
    )
    tamanios = {t.id: t.nombre for t in Tamanio.query.all()}
    colores = {c.id: c.nombre for c in Color.query.all()}

    out = []
    for d in dets:
        tname = tamanios.get(d.tamanio_id, "—")
        cname = colores.get(d.color_id, "—")
        precio = f"S/{float(d.precio):.2f}" if d.precio is not None else "—"
        cap = f" • {d.capacidad}" if d.capacidad else ""
        label = f"{cname} • {tname}{cap} — {precio}"
        out.append({"id": d.id, "label": label})
    return jsonify(out), 200
