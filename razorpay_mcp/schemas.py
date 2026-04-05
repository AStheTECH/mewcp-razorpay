from typing import Optional
from typing_extensions import TypedDict


class RazorpayAuth(TypedDict):
    """Razorpay API key credentials passed per request."""
    key_id: str
    key_secret: str


class OrderNotes(TypedDict, total=False):
    """Arbitrary key-value notes attached to an order or refund."""
    shipping_address: str
    merchant_order_id: str


class RefundNotes(TypedDict, total=False):
    """Arbitrary key-value notes attached to a refund."""
    notes_key_1: str
    notes_key_2: str
