# external_apis/coupons/coupons_gateway.py
from __future__ import annotations
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from decimal import Decimal

# importa tu client
from external_apis.coupons import coupons_client as cc

coupons_gateway_bp = Blueprint("coupons_gateway", __name__, url_prefix="/coupons-api")

# -------- Helpers --------
def _as_iso(dt) -> str | None:
    if not dt:
        return None
    if isinstance(dt, datetime):
        return dt.isoformat()
    return str(dt)

def _ok(status_code, body):
    return jsonify(body), status_code

def _from_client(resp_tuple):
    status, body = resp_tuple
    return jsonify(body), status

# ---------- Catálogos ----------
@coupons_gateway_bp.route("/coupon-types", methods=["GET"])
def gw_list_coupon_types():
    return _from_client(cc.list_coupon_types())

@coupons_gateway_bp.route("/discount-types", methods=["GET"])
def gw_list_discount_types():
    # Asegúrate de tener esta función en coupons_client.py (la incluyo más abajo)
    return _from_client(cc.list_discount_types())

# ---------- Coupons ----------
@coupons_gateway_bp.route("/coupons", methods=["GET"])
def gw_list_coupons():
    business_id = request.args.get("business_id", type=int)
    code        = request.args.get("code", type=str)
    active_only = request.args.get("active_only", default="false").lower() in ("1","true","yes")
    return _from_client(cc.list_coupons(business_id, code, active_only))

@coupons_gateway_bp.route("/coupons", methods=["POST"])
def gw_create_coupon():
    data = request.get_json(silent=True) or {}
    return _from_client(cc.create_coupon(
        business_id       = int(data.get("business_id")),
        name              = data.get("name"),
        discount_type_id  = int(data.get("discount_type_id")),
        value             = data.get("value"),
        start_date        = data.get("start_date"),
        end_date          = data.get("end_date"),
        coupon_type_id    = data.get("coupon_type_id"),
        description       = data.get("description"),
        max_discount      = data.get("max_discount"),
        max_uses          = data.get("max_uses"),
        code              = data.get("code"),
        event_name        = data.get("event_name"),
        is_shared_alliances = bool(data.get("is_shared_alliances", False)),
        status            = data.get("status", "ACTIVE"),
    ))

@coupons_gateway_bp.route("/coupons/<int:coupon_id>", methods=["PUT"])
def gw_update_coupon(coupon_id: int):
    data = request.get_json(silent=True) or {}
    return _from_client(cc.update_coupon(
        coupon_id         = coupon_id,
        business_id       = int(data.get("business_id")),
        name              = data.get("name"),
        discount_type_id  = int(data.get("discount_type_id")),
        value             = data.get("value"),
        start_date        = data.get("start_date"),
        end_date          = data.get("end_date"),
        coupon_type_id    = data.get("coupon_type_id"),
        description       = data.get("description"),
        max_discount      = data.get("max_discount"),
        max_uses          = data.get("max_uses"),
        code              = data.get("code"),
        event_name        = data.get("event_name"),
        is_shared_alliances = bool(data.get("is_shared_alliances", False)),
        status            = data.get("status", "ACTIVE"),
    ))

@coupons_gateway_bp.route("/coupons/<int:coupon_id>", methods=["DELETE"])
def gw_delete_coupon(coupon_id: int):
    return _from_client(cc.delete_coupon(coupon_id))

@coupons_gateway_bp.route("/coupons/by-business/<int:business_id>", methods=["GET"])
def gw_coupons_by_business(business_id: int):
    return _from_client(cc.list_coupons_by_business(business_id))

# ---------- Coupon ↔ Product ----------
@coupons_gateway_bp.route("/coupon-products", methods=["POST"])
def gw_add_coupon_product():
    data = request.get_json(silent=True) or {}
    return _from_client(cc.add_coupon_product_mapping(
        coupon_id  = int(data.get("coupon_id")),
        product_id = int(data.get("product_id"))
    ))

@coupons_gateway_bp.route("/coupon-products/bulk", methods=["POST"])
def gw_bulk_coupon_product():
    data = request.get_json(silent=True) or {}
    return _from_client(cc.bulk_add_coupon_product_mappings(
        coupon_id   = int(data.get("coupon_id")),
        product_ids = list(map(int, data.get("product_ids") or []))
    ))

@coupons_gateway_bp.route("/coupon-products/by-coupon/<int:coupon_id>", methods=["GET"])
def gw_list_products_by_coupon(coupon_id: int):
    return _from_client(cc.list_products_by_coupon(coupon_id))

@coupons_gateway_bp.route("/coupon-products/by-product/<int:product_id>", methods=["GET"])
def gw_list_coupons_by_product(product_id: int):
    return _from_client(cc.list_coupons_by_product(product_id))

@coupons_gateway_bp.route("/coupon-products", methods=["DELETE"])
def gw_del_coupon_product():
    data = request.get_json(silent=True) or {}
    return _from_client(cc.remove_coupon_product_mapping(
        coupon_id  = int(data.get("coupon_id")),
        product_id = int(data.get("product_id"))
    ))

@coupons_gateway_bp.route("/coupon-products/by-coupon/<int:coupon_id>", methods=["DELETE"])
def gw_del_all_coupon_products(coupon_id: int):
    return _from_client(cc.remove_all_coupon_product_mappings_for_coupon(coupon_id))

# ---------- Trigger: buy X → grant Y ----------
@coupons_gateway_bp.route("/coupon-trigger-products", methods=["POST"])
def gw_add_trigger():
    data = request.get_json(silent=True) or {}
    return _from_client(cc.add_trigger_mapping(
        product_trigger_id = int(data.get("product_trigger_id")),
        coupon_id          = int(data.get("coupon_id")),
        min_quantity       = int(data.get("min_quantity", 1)),
        min_amount         = data.get("min_amount")
    ))

@coupons_gateway_bp.route("/coupon-trigger-products/bulk", methods=["POST"])
def gw_bulk_trigger():
    data = request.get_json(silent=True) or {}
    return _from_client(cc.bulk_add_trigger_mappings(
        coupon_id          = int(data.get("coupon_id")),
        product_trigger_ids= list(map(int, data.get("product_trigger_ids") or [])),
        min_quantity       = int(data.get("min_quantity", 1)),
        min_amount         = data.get("min_amount")
    ))

@coupons_gateway_bp.route("/coupon-trigger-products/by-coupon/<int:coupon_id>", methods=["GET"])
def gw_list_triggers_by_coupon(coupon_id: int):
    return _from_client(cc.list_triggers_by_coupon(coupon_id))

@coupons_gateway_bp.route("/coupon-trigger-products/by-trigger/<int:product_trigger_id>", methods=["GET"])
def gw_list_coupons_by_trigger(product_trigger_id: int):
    return _from_client(cc.list_coupons_by_trigger(product_trigger_id))

@coupons_gateway_bp.route("/coupon-trigger-products", methods=["DELETE"])
def gw_del_trigger():
    data = request.get_json(silent=True) or {}
    return _from_client(cc.remove_trigger_mapping(
        product_trigger_id = int(data.get("product_trigger_id")),
        coupon_id          = int(data.get("coupon_id"))
    ))

@coupons_gateway_bp.route("/coupon-trigger-products/by-coupon/<int:coupon_id>", methods=["DELETE"])
def gw_del_all_triggers(coupon_id: int):
    return _from_client(cc.remove_all_triggers_for_coupon(coupon_id))
