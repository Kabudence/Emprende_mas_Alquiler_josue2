# external_apis/coupons/coupons_client.py
import os
import json
import logging
from typing import Any, Dict, List, Optional, Tuple
import requests
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("coupons-api")

# MICRO (no gateway)
BASE_URL = os.getenv("COUPONS_BASE_URL", "http://127.0.0.1:5001")

COUPON_TYPES_PREFIX          = "/api/coupon-types"
COUPONS_PREFIX               = "/api/coupons"
COUPON_PRODUCTS_PREFIX       = "/api/coupon-products"
COUPON_TRIGGER_PRODUCTS_PREF = "/api/coupon-trigger-products"
COUPON_CLIENTS_PREFIX        = "/api/coupon-clients"
CATEGORIES_PREFIX            = "/api/coupon-categories"
EVENTS_PREFIX                = "/api/coupon-events"

DEFAULT_TIMEOUT = 10


def _resp_tuple(resp: requests.Response) -> Tuple[int, Any]:
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

# ---------------- COUPON TYPES ----------------
def create_coupon_type(name: str, description: Optional[str] = None):
    url = f"{BASE_URL}{COUPON_TYPES_PREFIX}"
    return _resp_tuple(_post(url, {"name": name, "description": description}))

def list_coupon_types():
    url = f"{BASE_URL}{COUPON_TYPES_PREFIX}"
    return _resp_tuple(_get(url))

def get_coupon_type(coupon_type_id: int):
    url = f"{BASE_URL}{COUPON_TYPES_PREFIX}/{coupon_type_id}"
    return _resp_tuple(_get(url))

def update_coupon_type(coupon_type_id: int, name: str, description: Optional[str] = None):
    url = f"{BASE_URL}{COUPON_TYPES_PREFIX}/{coupon_type_id}"
    return _resp_tuple(_put(url, {"name": name, "description": description}))

def delete_coupon_type(coupon_type_id: int):
    url = f"{BASE_URL}{COUPON_TYPES_PREFIX}/{coupon_type_id}"
    return _resp_tuple(_delete(url))

# ---------------- CATEGORIES ----------------
def create_category(name: str, description: Optional[str] = None):
    url = f"{BASE_URL}{CATEGORIES_PREFIX}"
    return _resp_tuple(_post(url, {"name": name, "description": description}))

def list_categories():
    url = f"{BASE_URL}{CATEGORIES_PREFIX}"
    return _resp_tuple(_get(url))

def get_category(category_id: int):
    url = f"{BASE_URL}{CATEGORIES_PREFIX}/{category_id}"
    return _resp_tuple(_get(url))

def update_category(category_id: int, name: str, description: Optional[str] = None):
    url = f"{BASE_URL}{CATEGORIES_PREFIX}/{category_id}"
    return _resp_tuple(_put(url, {"name": name, "description": description}))

def delete_category(category_id: int):
    url = f"{BASE_URL}{CATEGORIES_PREFIX}/{category_id}"
    return _resp_tuple(_delete(url))

# ---------------- EVENTS ----------------
def create_event(name: str, description: Optional[str] = None):
    url = f"{BASE_URL}{EVENTS_PREFIX}"
    return _resp_tuple(_post(url, {"name": name, "description": description}))

def list_events():
    url = f"{BASE_URL}{EVENTS_PREFIX}"
    return _resp_tuple(_get(url))

def get_event(event_id: int):
    url = f"{BASE_URL}{EVENTS_PREFIX}/{event_id}"
    return _resp_tuple(_get(url))

def update_event(event_id: int, name: str, description: Optional[str] = None):
    url = f"{BASE_URL}{EVENTS_PREFIX}/{event_id}"
    return _resp_tuple(_put(url, {"name": name, "description": description}))

def delete_event(event_id: int):
    url = f"{BASE_URL}{EVENTS_PREFIX}/{event_id}"
    return _resp_tuple(_delete(url))

# ---------------- COUPONS (sin status/max_uses) ----------------
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
    event_name: Optional[str] = None,
    is_shared_alliances: bool = False,
    category_id: Optional[int] = None,
    event_id: Optional[int] = None,
    show_in_coupon_holder: bool = False,
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
        "category_id": category_id,
        "event_id": event_id,
        "show_in_coupon_holder": show_in_coupon_holder,
        "description": description,
        "max_discount": max_discount,
        "event_name": event_name,
        "is_shared_alliances": is_shared_alliances,
    }
    return _resp_tuple(_post(url, payload))

def list_coupons(business_id: Optional[int] = None, active_only: bool = False):
    url = f"{BASE_URL}{COUPONS_PREFIX}"
    params: Dict[str, Any] = {}
    if business_id is not None:
        params["business_id"] = business_id
    if active_only:
        params["active_only"] = "true"
    return _resp_tuple(_get(url, params))

def get_coupon(coupon_id: int):
    url = f"{BASE_URL}{COUPONS_PREFIX}/{coupon_id}"
    return _resp_tuple(_get(url))

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
    event_name: Optional[str] = None,
    is_shared_alliances: bool = False,
    category_id: Optional[int] = None,
    event_id: Optional[int] = None,
    show_in_coupon_holder: bool = False,
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
        "category_id": category_id,
        "event_id": event_id,
        "show_in_coupon_holder": show_in_coupon_holder,
        "description": description,
        "max_discount": max_discount,
        "event_name": event_name,
        "is_shared_alliances": is_shared_alliances,
    }
    return _resp_tuple(_put(url, payload))

def delete_coupon(coupon_id: int):
    url = f"{BASE_URL}{COUPONS_PREFIX}/{coupon_id}"
    return _resp_tuple(_delete(url))

def list_coupons_by_business(business_id: int):
    url = f"{BASE_URL}{COUPONS_PREFIX}/by-business/{business_id}"
    return _resp_tuple(_get(url))

def list_active_coupons_now():
    url = f"{BASE_URL}{COUPONS_PREFIX}/active/now"
    return _resp_tuple(_get(url))

# ---------------- COUPON ↔ PRODUCT / SERVICE ----------------
def add_coupon_product_mapping(
    coupon_id: int,
    product_id: int,
    *,
    product_type: str,
    code: str,
    stock: Optional[int] = None,
    status: str = "ACTIVE"
):
    url = f"{BASE_URL}{COUPON_PRODUCTS_PREFIX}"
    payload: Dict[str, Any] = {
        "coupon_id": coupon_id,
        "product_id": product_id,
        "product_type": product_type,
        "code": code,
        "status": status
    }
    if stock is not None:
        payload["stock"] = stock
    return _resp_tuple(_post(url, payload))

def bulk_add_coupon_product_mappings(
    *,
    coupon_id: int,
    items: Optional[List[Dict[str, Any]]] = None,
    product_ids: Optional[List[int]] = None,
    product_type: Optional[str] = None,
    code: Optional[str] = None,
):
    url = f"{BASE_URL}{COUPON_PRODUCTS_PREFIX}/bulk"
    if items is None:
        items = [
            {"product_id": int(pid), "code": str(code), "product_type": str(product_type).upper()}
            for pid in (product_ids or [])
        ]
    payload = {"coupon_id": coupon_id, "items": items}
    return _resp_tuple(_post(url, payload))

def list_products_by_coupon(coupon_id: int):
    url = f"{BASE_URL}{COUPON_PRODUCTS_PREFIX}/by-coupon/{coupon_id}"
    return _resp_tuple(_get(url))

def list_coupons_by_product(product_id: int):
    url = f"{BASE_URL}{COUPON_PRODUCTS_PREFIX}/by-product/{product_id}"
    return _resp_tuple(_get(url))

def remove_coupon_product_mapping(coupon_id: int, product_id: int):
    url = f"{BASE_URL}{COUPON_PRODUCTS_PREFIX}"
    payload = {"coupon_id": coupon_id, "product_id": product_id}
    return _resp_tuple(_delete(url, payload))

def remove_all_coupon_product_mappings_for_coupon(coupon_id: int):
    url = f"{BASE_URL}{COUPON_PRODUCTS_PREFIX}/by-coupon/{coupon_id}"
    return _resp_tuple(_delete(url))

def decrement_coupon_product_stock(coupon_id: int, product_id: int, quantity: int = 1):
    url = f"{BASE_URL}{COUPON_PRODUCTS_PREFIX}/{coupon_id}/{product_id}/decrement"
    payload = {"quantity": int(quantity)}
    return _resp_tuple(_put(url, payload))

# ---------------- TRIGGERS ----------------
def add_trigger_mapping(
    product_trigger_id: int,
    coupon_id: int,
    *,
    product_type: str = "PRODUCT",
    min_quantity: int = 1,
    min_amount: Optional[Any] = None
):
    url = f"{BASE_URL}{COUPON_TRIGGER_PRODUCTS_PREF}"
    payload = {
        "product_trigger_id": product_trigger_id,
        "coupon_id": coupon_id,
        "product_type": product_type,
        "min_quantity": min_quantity,
        "min_amount": min_amount
    }
    return _resp_tuple(_post(url, payload))

def bulk_add_trigger_mappings(
    coupon_id: int,
    product_trigger_ids: List[int],
    *,
    product_type: str = "PRODUCT",
    min_quantity: int = 1,
    min_amount: Optional[Any] = None
):
    url = f"{BASE_URL}{COUPON_TRIGGER_PRODUCTS_PREF}/bulk"
    payload = {
        "coupon_id": coupon_id,
        "product_trigger_ids": product_trigger_ids,
        "product_type": product_type,
        "min_quantity": min_quantity,
        "min_amount": min_amount
    }
    return _resp_tuple(_post(url, payload))

def list_triggers_by_coupon(coupon_id: int):
    url = f"{BASE_URL}{COUPON_TRIGGER_PRODUCTS_PREF}/by-coupon/{coupon_id}"
    return _resp_tuple(_get(url))

def list_coupons_by_trigger(product_trigger_id: int):
    url = f"{BASE_URL}{COUPON_TRIGGER_PRODUCTS_PREF}/by-trigger/{product_trigger_id}"
    return _resp_tuple(_get(url))

def remove_trigger_mapping(product_trigger_id: int, coupon_id: int):
    url = f"{BASE_URL}{COUPON_TRIGGER_PRODUCTS_PREF}"
    payload = {"product_trigger_id": product_trigger_id, "coupon_id": coupon_id}
    return _resp_tuple(_delete(url, payload))

def remove_all_triggers_for_coupon(coupon_id: int):
    url = f"{BASE_URL}{COUPON_TRIGGER_PRODUCTS_PREF}/by-coupon/{coupon_id}"
    return _resp_tuple(_delete(url))



def list_triggers_by_items(*, business_id: Optional[int] = None, items: List[Dict[str, Any]] = []):
    """
    POST /api/coupon-trigger-products/by-items
    Body: {"business_id": <opt>, "items":[{"product_type":"PRODUCT","product_id":..., "quantity":..., "amount":...}, ...]}
    """
    url = f"{BASE_URL}{COUPON_TRIGGER_PRODUCTS_PREF}/by-items"
    payload: Dict[str, Any] = {"items": items}
    if business_id is not None:
        payload["business_id"] = int(business_id)
    return _resp_tuple(_post(url, payload))

def grant_coupon_to_client(
    *,
    coupon_id: int,
    client_id: int,
    business_id: int,
    origin: str = "TRIGGER",
    origin_ref: Optional[int] = None,
    expires_at: Optional[str] = None,
    uses_allowed: int = 1,
    code: Optional[str] = None,   # <-- NUEVO
):
    url = f"{BASE_URL}{COUPON_CLIENTS_PREFIX}"
    payload: Dict[str, Any] = {
        "coupon_id": int(coupon_id),
        "client_id": int(client_id),
        "business_id": int(business_id),
        "origin": origin,
        "origin_ref": origin_ref,
        "expires_at": expires_at,
        "uses_allowed": int(uses_allowed),
    }
    if code is not None:          # <-- NUEVO
        payload["code"] = code

    return _resp_tuple(_post(url, payload))


def list_coupon_clients(
    *,
    client_id: Optional[int] = None,
    business_id: Optional[int] = None,
    status: Optional[str] = None,
    active_only: bool = False
):
    url = f"{BASE_URL}{COUPON_CLIENTS_PREFIX}"
    params: Dict[str, Any] = {}
    if client_id is not None:
        params["client_id"] = int(client_id)
    if business_id is not None:
        params["business_id"] = int(business_id)
    if status:
        params["status"] = str(status)
    if active_only:
        params["active_only"] = "true"
    return _resp_tuple(_get(url, params))

def get_coupon_client(coupon_client_id: int):
    url = f"{BASE_URL}{COUPON_CLIENTS_PREFIX}/{coupon_client_id}"
    return _resp_tuple(_get(url))

def redeem_coupon_client(coupon_client_id: int, quantity: int = 1):
    url = f"{BASE_URL}{COUPON_CLIENTS_PREFIX}/{coupon_client_id}/redeem"
    payload = {"quantity": int(quantity)}
    return _resp_tuple(_put(url, payload))

def expire_coupon_client(coupon_client_id: int):
    url = f"{BASE_URL}{COUPON_CLIENTS_PREFIX}/{coupon_client_id}/expire"
    return _resp_tuple(_put(url, {}))

def delete_coupon_client(coupon_client_id: int):
    url = f"{BASE_URL}{COUPON_CLIENTS_PREFIX}/{coupon_client_id}"
    return _resp_tuple(_delete(url))

# ---------------- Discount types ----------------
def list_discount_types():
    url = f"{BASE_URL}/api/discount-types"
    return _resp_tuple(_get(url))

# ---------------- Health ----------------
def healthcheck():
    url = f"{BASE_URL}/health"
    return _resp_tuple(_get(url))
