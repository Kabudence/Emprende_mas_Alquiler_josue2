# coupons_client.py
import os
import json
import logging
from typing import Any, Dict, List, Optional, Tuple
import requests
from datetime import datetime

# ---------- Logging ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("coupons-api")

# ---------- Config ----------
BASE_URL = os.getenv("COUPONS_BASE_URL", "http://127.0.0.1:8000")
# Prefixes (de los blueprints que ya montaste)
COUPON_TYPES_PREFIX          = "/api/coupon-types"
COUPONS_PREFIX               = "/api/coupons"
COUPON_PRODUCTS_PREFIX       = "/api/coupon-products"
COUPON_TRIGGER_PRODUCTS_PREF = "/api/coupon-trigger-products"

DEFAULT_TIMEOUT = 10


# ----------------------------
# Helpers
# ----------------------------
def _resp_tuple(resp: requests.Response):
    """ Devuelve (status_code, json|texto). """
    log.info("← %s %s", resp.status_code, resp.text[:200])
    try:
        return resp.status_code, resp.json()
    except ValueError:
        return resp.status_code, resp.text


def _post(url: str, payload: Optional[Dict[str, Any]] = None, **kw):
    log.info("POST %s » %s", url, json.dumps(payload or {}, default=str))
    return requests.post(url, json=payload, timeout=kw.get("timeout", DEFAULT_TIMEOUT))

def _get(url: str, params: Optional[Dict[str, Any]] = None, **kw):
    log.info("GET  %s ? %s", url, json.dumps(params or {}, default=str))
    return requests.get(url, params=params, timeout=kw.get("timeout", DEFAULT_TIMEOUT))

def _put(url: str, payload: Optional[Dict[str, Any]] = None, **kw):
    log.info("PUT  %s » %s", url, json.dumps(payload or {}, default=str))
    return requests.put(url, json=payload, timeout=kw.get("timeout", DEFAULT_TIMEOUT))

def _delete(url: str, payload: Optional[Dict[str, Any]] = None, **kw):
    body_log = json.dumps(payload or {}, default=str) if payload is not None else ""
    log.info("DEL  %s » %s", url, body_log)
    return requests.delete(url, json=payload, timeout=kw.get("timeout", DEFAULT_TIMEOUT))


# ============================================================
# COUPON TYPES
# ============================================================
def create_coupon_type(name: str, description: Optional[str] = None):
    url = f"{BASE_URL}{COUPON_TYPES_PREFIX}"
    try:
        resp = _post(url, {"name": name, "description": description})
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def list_coupon_types():
    url = f"{BASE_URL}{COUPON_TYPES_PREFIX}"
    try:
        resp = _get(url)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def get_coupon_type(coupon_type_id: int):
    url = f"{BASE_URL}{COUPON_TYPES_PREFIX}/{coupon_type_id}"
    try:
        resp = _get(url)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def update_coupon_type(coupon_type_id: int, name: str, description: Optional[str] = None):
    url = f"{BASE_URL}{COUPON_TYPES_PREFIX}/{coupon_type_id}"
    try:
        resp = _put(url, {"name": name, "description": description})
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def delete_coupon_type(coupon_type_id: int):
    url = f"{BASE_URL}{COUPON_TYPES_PREFIX}/{coupon_type_id}"
    try:
        resp = _delete(url)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise


# ============================================================
# COUPONS (core)
# ============================================================
def create_coupon(
    business_id: int,
    name: str,
    discount_type_id: int,
    value: Any,
    start_date: datetime | str,
    end_date: datetime | str,
    coupon_type_id: Optional[int] = None,
    description: Optional[str] = None,
    max_discount: Optional[Any] = None,
    max_uses: Optional[int] = None,
    code: Optional[str] = None,
    event_name: Optional[str] = None,
    is_shared_alliances: bool = False,
    status: str = "ACTIVE",
):
    url = f"{BASE_URL}{COUPONS_PREFIX}"
    payload = {
        "business_id": business_id,
        "name": name,
        "discount_type_id": discount_type_id,
        "value": value,
        "start_date": start_date if isinstance(start_date, str) else start_date.isoformat(),
        "end_date": end_date if isinstance(end_date, str) else end_date.isoformat(),
        "coupon_type_id": coupon_type_id,
        "description": description,
        "max_discount": max_discount,
        "max_uses": max_uses,
        "code": code,
        "event_name": event_name,
        "is_shared_alliances": is_shared_alliances,
        "status": status,
    }
    try:
        resp = _post(url, payload)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def list_coupons(business_id: Optional[int] = None, code: Optional[str] = None, active_only: bool = False):
    url = f"{BASE_URL}{COUPONS_PREFIX}"
    params = {}
    if business_id is not None:
        params["business_id"] = business_id
    if code:
        params["code"] = code
    if active_only:
        params["active_only"] = "true"
    try:
        resp = _get(url, params)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def get_coupon(coupon_id: int):
    url = f"{BASE_URL}{COUPONS_PREFIX}/{coupon_id}"
    try:
        resp = _get(url)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def update_coupon(
    coupon_id: int,
    business_id: int,
    name: str,
    discount_type_id: int,
    value: Any,
    start_date: datetime | str,
    end_date: datetime | str,
    coupon_type_id: Optional[int] = None,
    description: Optional[str] = None,
    max_discount: Optional[Any] = None,
    max_uses: Optional[int] = None,
    code: Optional[str] = None,
    event_name: Optional[str] = None,
    is_shared_alliances: bool = False,
    status: str = "ACTIVE",
):
    url = f"{BASE_URL}{COUPONS_PREFIX}/{coupon_id}"
    payload = {
        "business_id": business_id,
        "name": name,
        "discount_type_id": discount_type_id,
        "value": value,
        "start_date": start_date if isinstance(start_date, str) else start_date.isoformat(),
        "end_date": end_date if isinstance(end_date, str) else end_date.isoformat(),
        "coupon_type_id": coupon_type_id,
        "description": description,
        "max_discount": max_discount,
        "max_uses": max_uses,
        "code": code,
        "event_name": event_name,
        "is_shared_alliances": is_shared_alliances,
        "status": status,
    }
    try:
        resp = _put(url, payload)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def delete_coupon(coupon_id: int):
    url = f"{BASE_URL}{COUPONS_PREFIX}/{coupon_id}"
    try:
        resp = _delete(url)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def find_coupon_by_code(code: str):
    url = f"{BASE_URL}{COUPONS_PREFIX}/by-code/{code}"
    try:
        resp = _get(url)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def list_coupons_by_business(business_id: int):
    url = f"{BASE_URL}{COUPONS_PREFIX}/by-business/{business_id}"
    try:
        resp = _get(url)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def list_active_coupons_now():
    url = f"{BASE_URL}{COUPONS_PREFIX}/active/now"
    try:
        resp = _get(url)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise


# ============================================================
# COUPON ↔ PRODUCT mappings
# ============================================================
def add_coupon_product_mapping(coupon_id: int, product_id: int):
    url = f"{BASE_URL}{COUPON_PRODUCTS_PREFIX}"
    payload = {"coupon_id": coupon_id, "product_id": product_id}
    try:
        resp = _post(url, payload)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def bulk_add_coupon_product_mappings(coupon_id: int, product_ids: List[int]):
    url = f"{BASE_URL}{COUPON_PRODUCTS_PREFIX}/bulk"
    payload = {"coupon_id": coupon_id, "product_ids": product_ids}
    try:
        resp = _post(url, payload)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def list_products_by_coupon(coupon_id: int):
    url = f"{BASE_URL}{COUPON_PRODUCTS_PREFIX}/by-coupon/{coupon_id}"
    try:
        resp = _get(url)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def list_coupons_by_product(product_id: int):
    url = f"{BASE_URL}{COUPON_PRODUCTS_PREFIX}/by-product/{product_id}"
    try:
        resp = _get(url)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def remove_coupon_product_mapping(coupon_id: int, product_id: int):
    url = f"{BASE_URL}{COUPON_PRODUCTS_PREFIX}"
    payload = {"coupon_id": coupon_id, "product_id": product_id}
    try:
        resp = _delete(url, payload)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def remove_all_coupon_product_mappings_for_coupon(coupon_id: int):
    url = f"{BASE_URL}{COUPON_PRODUCTS_PREFIX}/by-coupon/{coupon_id}"
    try:
        resp = _delete(url)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise


# ============================================================
# TRIGGER: buy product X → grant coupon Y
# ============================================================
def add_trigger_mapping(
    product_trigger_id: int,
    coupon_id: int,
    min_quantity: int = 1,
    min_amount: Optional[Any] = None
):
    url = f"{BASE_URL}{COUPON_TRIGGER_PRODUCTS_PREF}"
    payload = {
        "product_trigger_id": product_trigger_id,
        "coupon_id": coupon_id,
        "min_quantity": min_quantity,
        "min_amount": min_amount
    }
    try:
        resp = _post(url, payload)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def bulk_add_trigger_mappings(
    coupon_id: int,
    product_trigger_ids: List[int],
    min_quantity: int = 1,
    min_amount: Optional[Any] = None
):
    url = f"{BASE_URL}{COUPON_TRIGGER_PRODUCTS_PREF}/bulk"
    payload = {
        "coupon_id": coupon_id,
        "product_trigger_ids": product_trigger_ids,
        "min_quantity": min_quantity,
        "min_amount": min_amount
    }
    try:
        resp = _post(url, payload)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def list_triggers_by_coupon(coupon_id: int):
    url = f"{BASE_URL}{COUPON_TRIGGER_PRODUCTS_PREF}/by-coupon/{coupon_id}"
    try:
        resp = _get(url)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def list_coupons_by_trigger(product_trigger_id: int):
    url = f"{BASE_URL}{COUPON_TRIGGER_PRODUCTS_PREF}/by-trigger/{product_trigger_id}"
    try:
        resp = _get(url)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def remove_trigger_mapping(product_trigger_id: int, coupon_id: int):
    url = f"{BASE_URL}{COUPON_TRIGGER_PRODUCTS_PREF}"
    payload = {"product_trigger_id": product_trigger_id, "coupon_id": coupon_id}
    try:
        resp = _delete(url, payload)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

def remove_all_triggers_for_coupon(coupon_id: int):
    url = f"{BASE_URL}{COUPON_TRIGGER_PRODUCTS_PREF}/by-coupon/{coupon_id}"
    try:
        resp = _delete(url)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise

# === discount types ===
def list_discount_types():
    url = f"{BASE_URL}/api/discount-types"
    try:
        resp = _get(url)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise


# ============================================================
# Opcional: health
# ============================================================
def healthcheck():
    url = f"{BASE_URL}/health"
    try:
        resp = _get(url)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise


# ============================================================
# Mini-demo (ejecutar manualmente)
# ============================================================
if __name__ == "__main__":
    print("BASE_URL:", BASE_URL)
    sc, hb = healthcheck()
    print("health:", sc, hb)
    # sc, ct = create_coupon_type("SIMPLE", "simple coupons")
    # print("create_coupon_type:", sc, ct)
    # sc, lst = list_coupon_types()
    # print("list_coupon_types:", sc, lst)
