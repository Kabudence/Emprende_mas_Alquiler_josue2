# coupons/coupon/interface/coupon_ui.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

# Si usas SQLAlchemy del proyecto principal:
from app import db
from app.models import Negocio  # ajusta imports según tu app

# coupons/coupon/interface/coupon_ui.py
coupon_ui_bp = Blueprint("coupon_ui", __name__, url_prefix="/coupons")

def get_negocio():
    """Obtiene el negocio del usuario actual con SQLAlchemy (ajusta si tu modelo difiere)."""
    return Negocio.query.filter_by(usuario_id=current_user.id).first()

@coupon_ui_bp.route("/", methods=["GET"])
@login_required
def manage_coupons():
    negocio = get_negocio()
    if not negocio:
        flash("Primero debe crear un negocio.", "danger")
        return redirect(url_for("negocios.crear"))

    # Renderiza la UI; el JS hará fetch a las APIs REST del microservicio de cupones.
    # Pasamos negocio_id para filtrar “mis cupones”
    return render_template("slider/manage_coupons.html", negocio=negocio)
