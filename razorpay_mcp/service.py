import logging
from typing import Any, Optional

import httpx
from fastmcp_credentials import get_credentials

from .config import RAZORPAY_API_V1, RAZORPAY_API_V2

logger = logging.getLogger("razorpay-mcp-server")


def _get_auth() -> httpx.BasicAuth:
    """Build Basic Auth from injected Razorpay credentials."""
    cred = get_credentials()
    key_id = cred.fields.get("key_id")
    key_secret = cred.fields.get("key_secret")
    if not key_id:
        raise ValueError("No 'key_id' found in credentials")
    if not key_secret:
        raise ValueError("No 'key_secret' found in credentials")
    return httpx.BasicAuth(username=key_id, password=key_secret)


def _raise_for_error(response: httpx.Response) -> None:
    """Raise a RuntimeError with Razorpay error details when the response is not 2xx."""
    if response.is_error:
        try:
            body = response.json()
            err = body.get("error", {})
            msg = err.get("description", response.text)
            code = err.get("code", response.status_code)
        except Exception:
            msg = response.text
            code = response.status_code
        raise RuntimeError(f"Razorpay API error [{code}]: {msg}")


# ---------------------------------------------------------------------------
# Orders
# ---------------------------------------------------------------------------

def create_order(
    amount: int,
    currency: str,
    receipt: Optional[str] = None,
    notes: Optional[dict] = None,
    partial_payment: bool = False,
) -> dict[str, Any]:
    """Create a new Razorpay order."""
    payload: dict[str, Any] = {
        "amount": amount,
        "currency": currency,
        "partial_payment": partial_payment,
    }
    if receipt:
        payload["receipt"] = receipt
    if notes:
        payload["notes"] = notes

    with httpx.Client() as client:
        response = client.post(
            f"{RAZORPAY_API_V1}/orders",
            json=payload,
            auth=_get_auth(),
        )
    _raise_for_error(response)
    return response.json()


def fetch_order(order_id: str) -> dict[str, Any]:
    """Fetch a single order by ID."""
    with httpx.Client() as client:
        response = client.get(
            f"{RAZORPAY_API_V1}/orders/{order_id}",
            auth=_get_auth(),
        )
    _raise_for_error(response)
    return response.json()


def fetch_all_orders(
    count: int = 10,
    skip: int = 0,
    from_timestamp: Optional[int] = None,
    to_timestamp: Optional[int] = None,
) -> dict[str, Any]:
    """Fetch all orders with optional filters."""
    params: dict[str, Any] = {"count": count, "skip": skip}
    if from_timestamp:
        params["from"] = from_timestamp
    if to_timestamp:
        params["to"] = to_timestamp

    with httpx.Client() as client:
        response = client.get(
            f"{RAZORPAY_API_V1}/orders",
            params=params,
            auth=_get_auth(),
        )
    _raise_for_error(response)
    return response.json()


def fetch_payments_for_order(order_id: str) -> dict[str, Any]:
    """Fetch all payments linked to a specific order."""
    with httpx.Client() as client:
        response = client.get(
            f"{RAZORPAY_API_V1}/orders/{order_id}/payments",
            auth=_get_auth(),
        )
    _raise_for_error(response)
    return response.json()


def update_order(order_id: str, notes: dict[str, str]) -> dict[str, Any]:
    """Update notes on an existing order."""
    with httpx.Client() as client:
        response = client.patch(
            f"{RAZORPAY_API_V1}/orders/{order_id}",
            json={"notes": notes},
            auth=_get_auth(),
        )
    _raise_for_error(response)
    return response.json()


# ---------------------------------------------------------------------------
# Payments
# ---------------------------------------------------------------------------

def fetch_payment(payment_id: str) -> dict[str, Any]:
    """Fetch a single payment by ID."""
    with httpx.Client() as client:
        response = client.get(
            f"{RAZORPAY_API_V1}/payments/{payment_id}",
            auth=_get_auth(),
        )
    _raise_for_error(response)
    return response.json()


def fetch_all_payments(
    count: int = 10,
    skip: int = 0,
    from_timestamp: Optional[int] = None,
    to_timestamp: Optional[int] = None,
) -> dict[str, Any]:
    """Fetch all payments with optional filters."""
    params: dict[str, Any] = {"count": count, "skip": skip}
    if from_timestamp:
        params["from"] = from_timestamp
    if to_timestamp:
        params["to"] = to_timestamp

    with httpx.Client() as client:
        response = client.get(
            f"{RAZORPAY_API_V1}/payments",
            params=params,
            auth=_get_auth(),
        )
    _raise_for_error(response)
    return response.json()


def capture_payment(payment_id: str, amount: int, currency: str) -> dict[str, Any]:
    """Capture an authorized payment."""
    with httpx.Client() as client:
        response = client.post(
            f"{RAZORPAY_API_V1}/payments/{payment_id}/capture",
            json={"amount": amount, "currency": currency},
            auth=_get_auth(),
        )
    _raise_for_error(response)
    return response.json()


def update_payment(payment_id: str, notes: dict[str, str]) -> dict[str, Any]:
    """Update notes on an existing payment."""
    with httpx.Client() as client:
        response = client.patch(
            f"{RAZORPAY_API_V1}/payments/{payment_id}",
            json={"notes": notes},
            auth=_get_auth(),
        )
    _raise_for_error(response)
    return response.json()


# ---------------------------------------------------------------------------
# Refunds
# ---------------------------------------------------------------------------

def create_refund(
    payment_id: str,
    amount: Optional[int] = None,
    speed: str = "normal",
    notes: Optional[dict] = None,
    receipt: Optional[str] = None,
) -> dict[str, Any]:
    """Create a refund for a captured payment."""
    payload: dict[str, Any] = {"speed": speed}
    if amount:
        payload["amount"] = amount
    if notes:
        payload["notes"] = notes
    if receipt:
        payload["receipt"] = receipt

    with httpx.Client() as client:
        response = client.post(
            f"{RAZORPAY_API_V1}/payments/{payment_id}/refund",
            json=payload,
            auth=_get_auth(),
        )
    _raise_for_error(response)
    return response.json()


def fetch_refund(refund_id: str) -> dict[str, Any]:
    """Fetch a single refund by ID."""
    with httpx.Client() as client:
        response = client.get(
            f"{RAZORPAY_API_V1}/refunds/{refund_id}",
            auth=_get_auth(),
        )
    _raise_for_error(response)
    return response.json()


def fetch_all_refunds(
    count: int = 10,
    skip: int = 0,
    from_timestamp: Optional[int] = None,
    to_timestamp: Optional[int] = None,
) -> dict[str, Any]:
    """Fetch all refunds with optional filters."""
    params: dict[str, Any] = {"count": count, "skip": skip}
    if from_timestamp:
        params["from"] = from_timestamp
    if to_timestamp:
        params["to"] = to_timestamp

    with httpx.Client() as client:
        response = client.get(
            f"{RAZORPAY_API_V1}/refunds",
            params=params,
            auth=_get_auth(),
        )
    _raise_for_error(response)
    return response.json()


def fetch_refunds_for_payment(
    payment_id: str,
    count: int = 10,
    skip: int = 0,
) -> dict[str, Any]:
    """Fetch all refunds for a specific payment."""
    params: dict[str, Any] = {"count": count, "skip": skip}
    with httpx.Client() as client:
        response = client.get(
            f"{RAZORPAY_API_V1}/payments/{payment_id}/refunds",
            params=params,
            auth=_get_auth(),
        )
    _raise_for_error(response)
    return response.json()


def update_refund(refund_id: str, notes: dict[str, str]) -> dict[str, Any]:
    """Update notes on an existing refund."""
    with httpx.Client() as client:
        response = client.patch(
            f"{RAZORPAY_API_V1}/refunds/{refund_id}",
            json={"notes": notes},
            auth=_get_auth(),
        )
    _raise_for_error(response)
    return response.json()


# ---------------------------------------------------------------------------
# Settlements
# ---------------------------------------------------------------------------

def fetch_all_settlements(
    count: int = 10,
    skip: int = 0,
    from_timestamp: Optional[int] = None,
    to_timestamp: Optional[int] = None,
) -> dict[str, Any]:
    """Fetch all settlements."""
    params: dict[str, Any] = {"count": count, "skip": skip}
    if from_timestamp:
        params["from"] = from_timestamp
    if to_timestamp:
        params["to"] = to_timestamp

    with httpx.Client() as client:
        response = client.get(
            f"{RAZORPAY_API_V1}/settlements",
            params=params,
            auth=_get_auth(),
        )
    _raise_for_error(response)
    return response.json()


def fetch_settlement(settlement_id: str) -> dict[str, Any]:
    """Fetch a single settlement by ID."""
    with httpx.Client() as client:
        response = client.get(
            f"{RAZORPAY_API_V1}/settlements/{settlement_id}",
            auth=_get_auth(),
        )
    _raise_for_error(response)
    return response.json()
