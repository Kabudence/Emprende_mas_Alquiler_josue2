# external_apis/alianzas/alianza_client.py
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
log = logging.getLogger("alliances-api")

# ---------- Config ----------
# Apunta al BASE_URL del microservicio de alianzas (no al gateway interno).
BASE_URL = os.getenv("ALLIANCES_BASE_URL", "http://127.0.0.1:8000")

# Prefijo base expuesto por el microservicio
ALLIANCES_PREFIX = "/api/alliances"

DEFAULT_TIMEOUT = 10


# ----------------------------
# Helpers
# ----------------------------
def _resp_tuple(resp: requests.Response) -> Tuple[int, Any]:
    """Devuelve (status_code, json|texto)."""
    log.info("← %s %s", resp.status_code, resp.text[:200])
    try:
        return resp.status_code, resp.json()
    except ValueError:
        return resp.status_code, resp.text

def listar_por_negocio(negocio_id: int):
    # ANTES (provoca 404 porque el micro no tiene esta ruta):
    # url = f"{BASE_URL}{ALLIANCES_PREFIX}/by-business/{negocio_id}"
    # try:
    #     resp = _get(url)
    #     return _resp_tuple(resp)
    # except requests.RequestException as err:
    #     log.error("✖ network error: %s", err)
    #     raise

    # AHORA: usa la lista general con filtro por query param
    url = f"{BASE_URL}{ALLIANCES_PREFIX}"
    try:
        resp = _get(url, {"negocio_id": negocio_id})
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise



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
# CRUD / Solicitudes de alianza
# ============================================================
def solicitar_alianza(solicitante_negocio_id: int, receptor_negocio_id: int, motivo: Optional[str] = None):
    """
    Crea una solicitud de alianza (estado inicial: PENDIENTE).
    """
    url = f"{BASE_URL}{ALLIANCES_PREFIX}"
    payload = {
        "solicitante_negocio_id": solicitante_negocio_id,
        "receptor_negocio_id": receptor_negocio_id,
        "motivo": motivo,
    }
    try:
        resp = _post(url, payload)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise


def listar_alianzas(negocio_id: Optional[int] = None, estado: Optional[str] = None):
    """
    Lista alianzas globales o filtradas por negocio y/o estado.
    estado ∈ {'PENDIENTE','ACEPTADA','RECHAZADA','CANCELADA','SUSPENDIDA'}
    """
    url = f"{BASE_URL}{ALLIANCES_PREFIX}"
    params: Dict[str, Any] = {}
    if negocio_id is not None:
        params["negocio_id"] = negocio_id
    if estado:
        params["estado"] = estado
    try:
        resp = _get(url, params)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise


def obtener_alianza(alianza_id: int):
    url = f"{BASE_URL}{ALLIANCES_PREFIX}/{alianza_id}"
    try:
        resp = _get(url)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise





# ============================================================
# Bandejas / Consultas útiles
# ============================================================
def pendientes_recibidas(negocio_id: int):
    """
    Solicitudes PENDIENTE donde 'negocio_id' es receptor.
    """
    url = f"{BASE_URL}{ALLIANCES_PREFIX}/pending/received"
    params = {"negocio_id": negocio_id}
    try:
        resp = _get(url, params)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise


def pendientes_enviadas(negocio_id: int):
    """
    Solicitudes PENDIENTE donde 'negocio_id' es solicitante.
    """
    url = f"{BASE_URL}{ALLIANCES_PREFIX}/pending/sent"
    params = {"negocio_id": negocio_id}
    try:
        resp = _get(url, params)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise


def activas(negocio_id: int):
    """
    Alianzas en estado ACEPTADA para el negocio dado.
    """
    url = f"{BASE_URL}{ALLIANCES_PREFIX}/active"
    params = {"negocio_id": negocio_id}
    try:
        resp = _get(url, params)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise


def existe_entre(negocio_a: int, negocio_b: int):
    """
    Devuelve información/resumen si existe una relación (en cualquier estado) entre A y B.
    """
    url = f"{BASE_URL}{ALLIANCES_PREFIX}/exists"
    params = {"negocio_a": negocio_a, "negocio_b": negocio_b}
    try:
        resp = _get(url, params)
        return _resp_tuple(resp)
    except requests.RequestException as err:
        log.error("✖ network error: %s", err)
        raise


# ============================================================
# Transiciones de estado (aceptar / rechazar / cancelar / suspender / reactivar)
# ============================================================
def aceptar(alianza_id: int, actor_negocio_id: int, motivo: Optional[str] = None):
    url = f"{BASE_URL}{ALLIANCES_PREFIX}/{alianza_id}/aceptar"
    payload = {"actor_negocio_id": actor_negocio_id, "motivo": motivo}
    resp = _put(url, payload);  return _resp_tuple(resp)

def rechazar(alianza_id: int, actor_negocio_id: int, motivo: Optional[str] = None):
    url = f"{BASE_URL}{ALLIANCES_PREFIX}/{alianza_id}/rechazar"
    payload = {"actor_negocio_id": actor_negocio_id, "motivo": motivo}
    resp = _put(url, payload);  return _resp_tuple(resp)

def cancelar(alianza_id: int, actor_negocio_id: int, motivo: Optional[str] = None):
    url = f"{BASE_URL}{ALLIANCES_PREFIX}/{alianza_id}/cancelar"
    payload = {"actor_negocio_id": actor_negocio_id, "motivo": motivo}
    resp = _put(url, payload);  return _resp_tuple(resp)

def suspender(alianza_id: int, actor_negocio_id: int, motivo: Optional[str] = None):
    url = f"{BASE_URL}{ALLIANCES_PREFIX}/{alianza_id}/suspender"
    payload = {"actor_negocio_id": actor_negocio_id, "motivo": motivo}
    resp = _put(url, payload);  return _resp_tuple(resp)

def reactivar(alianza_id: int, actor_negocio_id: int, motivo: Optional[str] = None):
    url = f"{BASE_URL}{ALLIANCES_PREFIX}/{alianza_id}/reactivar"
    payload = {"actor_negocio_id": actor_negocio_id, "motivo": motivo}
    resp = _put(url, payload);  return _resp_tuple(resp)


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
    # sc, body = solicitar_alianza(1, 2, "hacer cross-sell")
    # print("solicitar:", sc, body)
    # sc, body = listar_por_negocio(1)
    # print("por negocio:", sc, body)
