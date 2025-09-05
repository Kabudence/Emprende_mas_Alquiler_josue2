from __future__ import annotations

from typing import Optional

from flask import Blueprint, request, jsonify
import logging

from external_apis.coupons import coupons_client as cc

coupons_gateway_bp = Blueprint("coupons_gateway", __name__, url_prefix="/coupons-api")
LOG = logging.getLogger("gw-coupons")
if not LOG.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S"))
    LOG.addHandler(_h)
LOG.setLevel(logging.INFO)

# ---- CORS para todo el gateway de cupones ----
@coupons_gateway_bp.after_request
def _add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    return resp

def _from_client(resp_tuple):
    status, body = resp_tuple
    return jsonify(body), status

# ---------- Catálogos ----------
@coupons_gateway_bp.route("/coupon-types", methods=["GET"])
def gw_list_coupon_types():
    return _from_client(cc.list_coupon_types())

@coupons_gateway_bp.route("/discount-types", methods=["GET"])
def gw_list_discount_types():
    return _from_client(cc.list_discount_types())

@coupons_gateway_bp.route("/categories", methods=["GET"])
def gw_list_categories():
    return _from_client(cc.list_categories())

@coupons_gateway_bp.route("/categories", methods=["POST"])
def gw_create_category():
    data = request.get_json(silent=True) or {}
    return _from_client(cc.create_category(data.get("name"), data.get("description")))

@coupons_gateway_bp.route("/categories/<int:category_id>", methods=["GET"])
def gw_get_category(category_id: int):
    return _from_client(cc.get_category(category_id))

@coupons_gateway_bp.route("/categories/<int:category_id>", methods=["PUT"])
def gw_update_category(category_id: int):
    data = request.get_json(silent=True) or {}
    return _from_client(cc.update_category(category_id, data.get("name"), data.get("description")))

@coupons_gateway_bp.route("/categories/<int:category_id>", methods=["DELETE"])
def gw_delete_category(category_id: int):
    return _from_client(cc.delete_category(category_id))

@coupons_gateway_bp.route("/events", methods=["GET"])
def gw_list_events():
    return _from_client(cc.list_events())

@coupons_gateway_bp.route("/events", methods=["POST"])
def gw_create_event():
    data = request.get_json(silent=True) or {}
    return _from_client(cc.create_event(data.get("name"), data.get("description")))

@coupons_gateway_bp.route("/events/<int:event_id>", methods=["GET"])
def gw_get_event(event_id: int):
    return _from_client(cc.get_event(event_id))

@coupons_gateway_bp.route("/events/<int:event_id>", methods=["PUT"])
def gw_update_event(event_id: int):
    data = request.get_json(silent=True) or {}
    return _from_client(cc.update_event(event_id, data.get("name"), data.get("description")))

@coupons_gateway_bp.route("/events/<int:event_id>", methods=["DELETE"])
def gw_delete_event(event_id: int):
    return _from_client(cc.delete_event(event_id))

# ---------- Coupons ----------
@coupons_gateway_bp.route("/coupons", methods=["GET"])
def gw_list_coupons():
    business_id = request.args.get("business_id", type=int)
    active_only = request.args.get("active_only", default="false").lower() in ("1", "true", "yes")
    return _from_client(cc.list_coupons(business_id, active_only))

@coupons_gateway_bp.route("/coupons", methods=["POST"])
def gw_create_coupon():
    d = request.get_json(silent=True) or {}
    return _from_client(cc.create_coupon(
        business_id=int(d.get("business_id")),
        name=d.get("name"),
        discount_type_id=int(d.get("discount_type_id")),
        value=d.get("value"),
        start_date=d.get("start_date"),
        end_date=d.get("end_date"),
        coupon_type_id=d.get("coupon_type_id"),
        category_id=d.get("category_id"),
        event_id=d.get("event_id"),
        show_in_coupon_holder=bool(d.get("show_in_coupon_holder", False)),
        description=d.get("description"),
        max_discount=d.get("max_discount"),
        event_name=d.get("event_name"),
        is_shared_alliances=bool(d.get("is_shared_alliances", False)),
    ))

@coupons_gateway_bp.route("/coupons/<int:coupon_id>", methods=["PUT"])
def gw_update_coupon(coupon_id: int):
    d = request.get_json(silent=True) or {}
    return _from_client(cc.update_coupon(
        coupon_id=coupon_id,
        business_id=int(d.get("business_id")),
        name=d.get("name"),
        discount_type_id=int(d.get("discount_type_id")),
        value=d.get("value"),
        start_date=d.get("start_date"),
        end_date=d.get("end_date"),
        coupon_type_id=d.get("coupon_type_id"),
        category_id=d.get("category_id"),
        event_id=d.get("event_id"),
        show_in_coupon_holder=bool(d.get("show_in_coupon_holder", False)),
        description=d.get("description"),
        max_discount=d.get("max_discount"),
        event_name=d.get("event_name"),
        is_shared_alliances=bool(d.get("is_shared_alliances", False)),
    ))

@coupons_gateway_bp.route("/coupons/<int:coupon_id>", methods=["DELETE"])
def gw_delete_coupon(coupon_id: int):
    return _from_client(cc.delete_coupon(coupon_id))

@coupons_gateway_bp.route("/coupons/by-business/<int:business_id>", methods=["GET"])
def gw_coupons_by_business(business_id: int):
    return _from_client(cc.list_coupons_by_business(business_id))

# ---------- Coupon ↔ Product/Service ----------
@coupons_gateway_bp.route("/coupon-products", methods=["POST"])
def gw_add_coupon_product():
    d = request.get_json(silent=True) or {}
    return _from_client(cc.add_coupon_product_mapping(
        coupon_id=int(d.get("coupon_id")),
        product_id=int(d.get("product_id")),
        product_type=str(d.get("product_type") or d.get("type") or "PRODUCT").upper(),
        code=str(d.get("code") or ""),
        stock=(int(d["stock"]) if d.get("stock") is not None else None),
        status=str(d.get("status", "ACTIVE")).upper()
    ))

@coupons_gateway_bp.route("/coupon-products/bulk", methods=["POST"])
def gw_bulk_coupon_product():
    d = request.get_json(silent=True) or {}

    items = d.get("items")
    if items is not None and isinstance(items, list):
        norm_items = []
        for it in items:
            if not isinstance(it, dict):
                continue
            obj = dict(it)
            if "product_type" in obj and isinstance(obj["product_type"], str):
                obj["product_type"] = obj["product_type"].upper()
            norm_items.append(obj)
        return _from_client(cc.bulk_add_coupon_product_mappings(
            coupon_id=int(d.get("coupon_id")),
            items=norm_items
        ))

    product_ids = d.get("product_ids")
    if product_ids is None and isinstance(d.get("items"), list):
        product_ids = [i for i in d.get("items") if isinstance(i, int)]

    return _from_client(cc.bulk_add_coupon_product_mappings(
        coupon_id=int(d.get("coupon_id")),
        product_ids=[int(pid) for pid in (product_ids or [])],
        product_type=str(d.get("product_type") or d.get("type") or "PRODUCT").upper(),
        code=str(d.get("code") or "")
    ))

@coupons_gateway_bp.route("/coupon-products/by-coupon/<int:coupon_id>", methods=["GET"])
def gw_list_products_by_coupon(coupon_id: int):
    return _from_client(cc.list_products_by_coupon(coupon_id))

@coupons_gateway_bp.route("/coupon-products/by-product/<int:product_id>", methods=["GET"])
def gw_list_coupons_by_product(product_id: int):
    return _from_client(cc.list_coupons_by_product(product_id))

@coupons_gateway_bp.route("/coupon-products", methods=["DELETE"])
def gw_del_coupon_product():
    d = request.get_json(silent=True) or {}
    return _from_client(cc.remove_coupon_product_mapping(
        coupon_id=int(d.get("coupon_id")),
        product_id=int(d.get("product_id"))
    ))

@coupons_gateway_bp.route("/coupon-products/by-coupon/<int:coupon_id>", methods=["DELETE"])
def gw_del_all_coupon_products(coupon_id: int):
    return _from_client(cc.remove_all_coupon_product_mappings_for_coupon(coupon_id))

@coupons_gateway_bp.route("/coupon-products/<int:coupon_id>/<int:product_id>/decrement", methods=["PUT"])
def gw_decrement_coupon_product_stock(coupon_id: int, product_id: int):
    d = request.get_json(silent=True) or {}
    qty = int(d.get("quantity", 1))
    return _from_client(cc.decrement_coupon_product_stock(coupon_id, product_id, qty))

# ---------- Trigger: buy X → grant Y ----------
@coupons_gateway_bp.route("/coupon-trigger-products", methods=["POST"])
def gw_add_trigger():
    d = request.get_json(silent=True) or {}
    return _from_client(cc.add_trigger_mapping(
        product_trigger_id=int(d.get("product_trigger_id")),
        coupon_id=int(d.get("coupon_id")),
        product_type=str(d.get("product_type") or d.get("type") or "PRODUCT").upper(),
        min_quantity=int(d.get("min_quantity", 1)),
        min_amount=d.get("min_amount")
    ))

@coupons_gateway_bp.route("/coupon-trigger-products/bulk", methods=["POST"])
def gw_bulk_trigger():
    d = request.get_json(silent=True) or {}
    return _from_client(cc.bulk_add_trigger_mappings(
        coupon_id=int(d.get("coupon_id")),
        product_trigger_ids=list(map(int, d.get("product_trigger_ids") or [])),
        product_type=str(d.get("product_type") or d.get("type") or "PRODUCT").upper(),
        min_quantity=int(d.get("min_quantity", 1)),
        min_amount=d.get("min_amount")
    ))

@coupons_gateway_bp.route("/coupon-trigger-products/by-coupon/<int:coupon_id>", methods=["GET"])
def gw_list_triggers_by_coupon(coupon_id: int):
    return _from_client(cc.list_triggers_by_coupon(coupon_id))

@coupons_gateway_bp.route("/coupon-trigger-products/by-trigger/<int:product_trigger_id>", methods=["GET"])
def gw_list_coupons_by_trigger(product_trigger_id: int):
    return _from_client(cc.list_coupons_by_trigger(product_trigger_id))

@coupons_gateway_bp.route("/coupon-trigger-products", methods=["DELETE"])
def gw_del_trigger():
    d = request.get_json(silent=True) or {}
    return _from_client(cc.remove_trigger_mapping(
        product_trigger_id=int(d.get("product_trigger_id")),
        coupon_id=int(d.get("coupon_id"))
    ))

@coupons_gateway_bp.route("/coupon-trigger-products/by-coupon/<int:coupon_id>", methods=["DELETE"])
def gw_del_all_triggers(coupon_id: int):
    return _from_client(cc.remove_all_triggers_for_coupon(coupon_id))

# -------- NUEVO: resolver triggers por lista de items --------
@coupons_gateway_bp.route("/coupon-trigger-products/by-items", methods=["POST"])
def gw_resolve_triggers_by_items():
    d = request.get_json(silent=True) or {}
    business_id = d.get("business_id")
    items = d.get("items") or []
    return _from_client(cc.list_triggers_by_items(business_id=business_id, items=items))


@coupons_gateway_bp.route("/coupon-clients", methods=["POST"])
def gw_grant_coupon_to_client():
    d = request.get_json(silent=True) or {}
    return _from_client(cc.grant_coupon_to_client(
        coupon_id=int(d.get("coupon_id")),
        client_id=int(d.get("client_id")),
        business_id=int(d.get("business_id")),
        origin=str(d.get("origin", "TRIGGER")),
        origin_ref=d.get("origin_ref"),
        expires_at=d.get("expires_at"),
        uses_allowed=int(d.get("uses_allowed", 1)),
        code=d.get("code"),                     # <-- NUEVO
    ))


@coupons_gateway_bp.route("/coupon-clients", methods=["GET"])
def gw_list_coupon_clients():
    client_id   = request.args.get("client_id", type=int)
    business_id = request.args.get("business_id", type=int)
    status      = request.args.get("status", type=str)
    active_only = request.args.get("active_only", default="false").lower() in ("1", "true", "yes")
    return _from_client(cc.list_coupon_clients(
        client_id=client_id,
        business_id=business_id,
        status=status,
        active_only=active_only
    ))

@coupons_gateway_bp.route("/coupon-clients/<int:coupon_client_id>", methods=["GET"])
def gw_get_coupon_client(coupon_client_id: int):
    return _from_client(cc.get_coupon_client(coupon_client_id))

@coupons_gateway_bp.route("/coupon-clients/<int:coupon_client_id>/redeem", methods=["PUT"])
def gw_redeem_coupon_client(coupon_client_id: int):
    d = request.get_json(silent=True) or {}
    qty = int(d.get("quantity", 1))
    return _from_client(cc.redeem_coupon_client(coupon_client_id, qty))

@coupons_gateway_bp.route("/coupon-clients/<int:coupon_client_id>/expire", methods=["PUT"])
def gw_expire_coupon_client(coupon_client_id: int):
    return _from_client(cc.expire_coupon_client(coupon_client_id))

@coupons_gateway_bp.route("/coupon-clients/<int:coupon_client_id>", methods=["DELETE"])
def gw_delete_coupon_client(coupon_client_id: int):
    return _from_client(cc.delete_coupon_client(coupon_client_id))

# ======== (Opcional) Orquestador para otorgar cupones al cerrar pago ========
@coupons_gateway_bp.route("/grants/for-order", methods=["POST", "OPTIONS"])
def gw_grants_for_order():
    if request.method == "OPTIONS":
        return ("", 204)

    d = request.get_json(silent=True) or {}
    business_id = int(d.get("business_id"))
    client_id   = int(d.get("client_id"))
    order_id    = int(d.get("order_id"))
    items       = list(d.get("items") or [])
    uses_allowed = int(d.get("uses_allowed", 1))
    expires_at   = d.get("expires_at")

    LOG.info("grants/for-order | req business_id=%s client_id=%s order_id=%s items=%s",
             business_id, client_id, order_id, items)

    st, body = cc.list_triggers_by_items(business_id=business_id, items=items)
    if st >= 400:
        LOG.warning("grants/for-order | resolver ERROR %s body=%s", st, body)
        return jsonify({"error": "cannot resolve triggers", "details": body}), st

    resolved = body if isinstance(body, list) else []
    LOG.info("grants/for-order | resolved=%s", resolved)

    granted = []
    errors  = []

    for r in resolved:
        try:
            coupon_id = int(r.get("coupon_id"))
            r_pid = r.get("product_id")
            r_ptype = r.get("product_type")

            # Elegimos el code desde coupon-products
            code = _pick_code_for_coupon(coupon_id, product_id=r_pid, product_type=r_ptype)
            if not code:
                LOG.warning("grants/for-order | NO CODE FOUND for coupon_id=%s (trigger pid=%s, type=%s)",
                            coupon_id, r_pid, r_ptype)
                errors.append({"coupon_id": coupon_id, "error": "no code mapping found"})
                continue

            LOG.info("grants/for-order | granting coupon_id=%s → client_id=%s (code=%s)",
                     coupon_id, client_id, code)

            st2, b2 = cc.grant_coupon_to_client(
                coupon_id=coupon_id,
                client_id=client_id,
                business_id=business_id,
                origin="TRIGGER",
                origin_ref=order_id,
                expires_at=expires_at,
                uses_allowed=uses_allowed,
                code=code,  # <-- ENVIAMOS CODE
            )
            if 200 <= st2 < 300:
                granted.append(b2)
            else:
                LOG.warning("grants/for-order | grant FAIL coupon_id=%s status=%s body=%s",
                            coupon_id, st2, b2)
                errors.append({"coupon_id": coupon_id, "status": st2, "body": b2})
        except Exception as ex:
            LOG.exception("grants/for-order | grant EXCEPTION coupon_id=%s", r.get("coupon_id"))
            errors.append({"coupon_id": r.get("coupon_id"), "error": str(ex)})

    resp = {"resolved": resolved, "granted": granted, "errors": errors}
    LOG.info("grants/for-order | resp=%s", resp)
    return jsonify(resp), 200 if not errors else 207

@coupons_gateway_bp.route("/coupons/<int:coupon_id>", methods=["GET"])
def gw_get_coupon(coupon_id: int):
    return _from_client(cc.get_coupon(coupon_id))

def _pick_code_for_coupon(coupon_id: int, *, product_id: Optional[int], product_type: Optional[str]) -> Optional[str]:
    """
    Busca un code en los mappings coupon_products del cupón.
    Preferencias:
      1) mapping que matchee product_id y product_type del trigger
      2) si sólo hay 1 mapping, usar su code
      3) primer mapping ACTIVE
      4) primer mapping disponible
    """
    st, rows = cc.list_products_by_coupon(coupon_id)
    if st >= 400 or not isinstance(rows, list) or not rows:
        return None

    pt = (product_type or "PRODUCT").upper()

    # 1) match exacto product_id + product_type
    for e in rows:
        try:
            pid = int(e.get("product_id"))
        except Exception:
            pid = None
        et = str(e.get("product_type") or "PRODUCT").upper()
        if pid == (int(product_id) if product_id is not None else None) and et == pt:
            code = e.get("code")
            if code:
                return code

    # 2) único mapping
    if len(rows) == 1 and rows[0].get("code"):
        return rows[0]["code"]

    # 3) primer ACTIVE
    for e in rows:
        if str(e.get("status", "ACTIVE")).upper() == "ACTIVE" and e.get("code"):
            return e["code"]

    # 4) cualquiera con code
    for e in rows:
        if e.get("code"):
            return e["code"]

    return None
