import json
import logging
from typing import Optional

from fastmcp import FastMCP
from pydantic import Field

from .service import (
    # Orders
    create_order,
    fetch_order,
    fetch_all_orders,
    fetch_payments_for_order,
    update_order,
    # Payments
    fetch_payment,
    fetch_all_payments,
    capture_payment,
    update_payment,
    # Refunds
    create_refund,
    fetch_refund,
    fetch_all_refunds,
    fetch_refunds_for_payment,
    update_refund,
    # Settlements
    fetch_all_settlements,
    fetch_settlement,
)

logger = logging.getLogger("razorpay-mcp-server")


def register_tools(mcp: FastMCP) -> None:

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    @mcp.tool(
        name="health_check",
        description="Check server readiness and basic connectivity.",
    )
    def health_check() -> str:
        return json.dumps({"status": "ok", "server": "CL Razorpay MCP Server"})

    # ------------------------------------------------------------------
    # Orders
    # ------------------------------------------------------------------

    @mcp.tool(
        name="create_order",
        description=(
            "Create a new Razorpay order. Amount must be in the smallest currency unit "
            "(e.g. paise for INR). Returns the order object including the order ID required "
            "to initiate a payment on the frontend."
        ),
    )
    def tool_create_order(
        key_id: str = Field(..., description="Razorpay API key ID"),
        key_secret: str = Field(..., description="Razorpay API key secret"),
        amount: int = Field(..., description="Amount in smallest currency unit (e.g. paise for INR)"),
        currency: str = Field(..., description="ISO 4217 currency code, e.g. 'INR'"),
        receipt: Optional[str] = Field(None, description="Merchant receipt number (max 40 chars)"),
        notes: Optional[dict] = Field(None, description="Key-value notes to attach to the order"),
        partial_payment: bool = Field(False, description="Whether partial payments are allowed"),
    ) -> str:
        try:
            result = create_order(
                key_id, key_secret, amount, currency, receipt, notes, partial_payment
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Failed create_order (amount={amount}, currency={currency}): {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="fetch_order",
        description="Fetch the details of a specific Razorpay order by its order ID.",
    )
    def tool_fetch_order(
        key_id: str = Field(..., description="Razorpay API key ID"),
        key_secret: str = Field(..., description="Razorpay API key secret"),
        order_id: str = Field(..., description="Razorpay order ID (e.g. 'order_XXXXXXXXXX')"),
    ) -> str:
        try:
            result = fetch_order(key_id, key_secret, order_id)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Failed fetch_order for '{order_id}': {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="fetch_all_orders",
        description=(
            "Fetch a paginated list of all Razorpay orders. Supports optional Unix timestamp "
            "range filters and pagination via count/skip."
        ),
    )
    def tool_fetch_all_orders(
        key_id: str = Field(..., description="Razorpay API key ID"),
        key_secret: str = Field(..., description="Razorpay API key secret"),
        count: int = Field(10, description="Number of orders to fetch (max 100)"),
        skip: int = Field(0, description="Number of orders to skip for pagination"),
        from_timestamp: Optional[int] = Field(None, description="Unix timestamp — fetch orders created after this time"),
        to_timestamp: Optional[int] = Field(None, description="Unix timestamp — fetch orders created before this time"),
    ) -> str:
        try:
            result = fetch_all_orders(
                key_id, key_secret, count, skip, from_timestamp, to_timestamp
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Failed fetch_all_orders: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="fetch_payments_for_order",
        description="Fetch all payments made against a specific Razorpay order ID.",
    )
    def tool_fetch_payments_for_order(
        key_id: str = Field(..., description="Razorpay API key ID"),
        key_secret: str = Field(..., description="Razorpay API key secret"),
        order_id: str = Field(..., description="Razorpay order ID (e.g. 'order_XXXXXXXXXX')"),
    ) -> str:
        try:
            result = fetch_payments_for_order(key_id, key_secret, order_id)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Failed fetch_payments_for_order for '{order_id}': {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="update_order",
        description="Update the notes field on an existing Razorpay order.",
    )
    def tool_update_order(
        key_id: str = Field(..., description="Razorpay API key ID"),
        key_secret: str = Field(..., description="Razorpay API key secret"),
        order_id: str = Field(..., description="Razorpay order ID (e.g. 'order_XXXXXXXXXX')"),
        notes: dict = Field(..., description="Key-value notes to update on the order"),
    ) -> str:
        try:
            result = update_order(key_id, key_secret, order_id, notes)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Failed update_order for '{order_id}': {e}")
            return json.dumps({"error": str(e)})

    # ------------------------------------------------------------------
    # Payments
    # ------------------------------------------------------------------

    @mcp.tool(
        name="fetch_payment",
        description="Fetch the details of a specific Razorpay payment by its payment ID.",
    )
    def tool_fetch_payment(
        key_id: str = Field(..., description="Razorpay API key ID"),
        key_secret: str = Field(..., description="Razorpay API key secret"),
        payment_id: str = Field(..., description="Razorpay payment ID (e.g. 'pay_XXXXXXXXXX')"),
    ) -> str:
        try:
            result = fetch_payment(key_id, key_secret, payment_id)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Failed fetch_payment for '{payment_id}': {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="fetch_all_payments",
        description=(
            "Fetch a paginated list of all Razorpay payments. Supports optional Unix timestamp "
            "range filters and pagination via count/skip."
        ),
    )
    def tool_fetch_all_payments(
        key_id: str = Field(..., description="Razorpay API key ID"),
        key_secret: str = Field(..., description="Razorpay API key secret"),
        count: int = Field(10, description="Number of payments to fetch (max 100)"),
        skip: int = Field(0, description="Number of payments to skip for pagination"),
        from_timestamp: Optional[int] = Field(None, description="Unix timestamp — fetch payments created after this time"),
        to_timestamp: Optional[int] = Field(None, description="Unix timestamp — fetch payments created before this time"),
    ) -> str:
        try:
            result = fetch_all_payments(
                key_id, key_secret, count, skip, from_timestamp, to_timestamp
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Failed fetch_all_payments: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="capture_payment",
        description=(
            "Capture an authorized Razorpay payment. Only payments in 'authorized' state can be "
            "captured. Amount must match the authorized amount exactly."
        ),
    )
    def tool_capture_payment(
        key_id: str = Field(..., description="Razorpay API key ID"),
        key_secret: str = Field(..., description="Razorpay API key secret"),
        payment_id: str = Field(..., description="Razorpay payment ID (e.g. 'pay_XXXXXXXXXX')"),
        amount: int = Field(..., description="Amount to capture in smallest currency unit (must match authorized amount)"),
        currency: str = Field(..., description="ISO 4217 currency code, e.g. 'INR'"),
    ) -> str:
        try:
            result = capture_payment(key_id, key_secret, payment_id, amount, currency)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Failed capture_payment for '{payment_id}': {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="update_payment",
        description="Update the notes field on an existing Razorpay payment.",
    )
    def tool_update_payment(
        key_id: str = Field(..., description="Razorpay API key ID"),
        key_secret: str = Field(..., description="Razorpay API key secret"),
        payment_id: str = Field(..., description="Razorpay payment ID (e.g. 'pay_XXXXXXXXXX')"),
        notes: dict = Field(..., description="Key-value notes to update on the payment"),
    ) -> str:
        try:
            result = update_payment(key_id, key_secret, payment_id, notes)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Failed update_payment for '{payment_id}': {e}")
            return json.dumps({"error": str(e)})

    # ------------------------------------------------------------------
    # Refunds
    # ------------------------------------------------------------------

    @mcp.tool(
        name="create_refund",
        description=(
            "Create a full or partial refund for a captured Razorpay payment. "
            "Omit amount for a full refund. Speed can be 'normal' or 'optimum'."
        ),
    )
    def tool_create_refund(
        key_id: str = Field(..., description="Razorpay API key ID"),
        key_secret: str = Field(..., description="Razorpay API key secret"),
        payment_id: str = Field(..., description="Razorpay payment ID to refund (e.g. 'pay_XXXXXXXXXX')"),
        amount: Optional[int] = Field(None, description="Refund amount in smallest currency unit; omit for full refund"),
        speed: str = Field("normal", description="Refund speed: 'normal' (default) or 'optimum'"),
        notes: Optional[dict] = Field(None, description="Key-value notes to attach to the refund"),
        receipt: Optional[str] = Field(None, description="Unique merchant receipt number for the refund"),
    ) -> str:
        try:
            result = create_refund(
                key_id, key_secret, payment_id, amount, speed, notes, receipt
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Failed create_refund for payment '{payment_id}': {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="fetch_refund",
        description="Fetch the details of a specific Razorpay refund by its refund ID.",
    )
    def tool_fetch_refund(
        key_id: str = Field(..., description="Razorpay API key ID"),
        key_secret: str = Field(..., description="Razorpay API key secret"),
        refund_id: str = Field(..., description="Razorpay refund ID (e.g. 'rfnd_XXXXXXXXXX')"),
    ) -> str:
        try:
            result = fetch_refund(key_id, key_secret, refund_id)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Failed fetch_refund for '{refund_id}': {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="fetch_all_refunds",
        description=(
            "Fetch a paginated list of all Razorpay refunds. Supports optional Unix timestamp "
            "range filters and pagination via count/skip."
        ),
    )
    def tool_fetch_all_refunds(
        key_id: str = Field(..., description="Razorpay API key ID"),
        key_secret: str = Field(..., description="Razorpay API key secret"),
        count: int = Field(10, description="Number of refunds to fetch (max 100)"),
        skip: int = Field(0, description="Number of refunds to skip for pagination"),
        from_timestamp: Optional[int] = Field(None, description="Unix timestamp — fetch refunds created after this time"),
        to_timestamp: Optional[int] = Field(None, description="Unix timestamp — fetch refunds created before this time"),
    ) -> str:
        try:
            result = fetch_all_refunds(
                key_id, key_secret, count, skip, from_timestamp, to_timestamp
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Failed fetch_all_refunds: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="fetch_refunds_for_payment",
        description="Fetch all refunds associated with a specific Razorpay payment ID.",
    )
    def tool_fetch_refunds_for_payment(
        key_id: str = Field(..., description="Razorpay API key ID"),
        key_secret: str = Field(..., description="Razorpay API key secret"),
        payment_id: str = Field(..., description="Razorpay payment ID (e.g. 'pay_XXXXXXXXXX')"),
        count: int = Field(10, description="Number of refunds to fetch (max 100)"),
        skip: int = Field(0, description="Number of refunds to skip for pagination"),
    ) -> str:
        try:
            result = fetch_refunds_for_payment(key_id, key_secret, payment_id, count, skip)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Failed fetch_refunds_for_payment for '{payment_id}': {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="update_refund",
        description="Update the notes field on an existing Razorpay refund.",
    )
    def tool_update_refund(
        key_id: str = Field(..., description="Razorpay API key ID"),
        key_secret: str = Field(..., description="Razorpay API key secret"),
        refund_id: str = Field(..., description="Razorpay refund ID (e.g. 'rfnd_XXXXXXXXXX')"),
        notes: dict = Field(..., description="Key-value notes to update on the refund"),
    ) -> str:
        try:
            result = update_refund(key_id, key_secret, refund_id, notes)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Failed update_refund for '{refund_id}': {e}")
            return json.dumps({"error": str(e)})

    # ------------------------------------------------------------------
    # Settlements
    # ------------------------------------------------------------------

    @mcp.tool(
        name="fetch_all_settlements",
        description=(
            "Fetch a paginated list of all Razorpay settlements. Supports optional Unix timestamp "
            "range filters and pagination via count/skip."
        ),
    )
    def tool_fetch_all_settlements(
        key_id: str = Field(..., description="Razorpay API key ID"),
        key_secret: str = Field(..., description="Razorpay API key secret"),
        count: int = Field(10, description="Number of settlements to fetch (max 100)"),
        skip: int = Field(0, description="Number of settlements to skip for pagination"),
        from_timestamp: Optional[int] = Field(None, description="Unix timestamp — fetch settlements created after this time"),
        to_timestamp: Optional[int] = Field(None, description="Unix timestamp — fetch settlements created before this time"),
    ) -> str:
        try:
            result = fetch_all_settlements(
                key_id, key_secret, count, skip, from_timestamp, to_timestamp
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Failed fetch_all_settlements: {e}")
            return json.dumps({"error": str(e)})

    @mcp.tool(
        name="fetch_settlement",
        description="Fetch the details of a specific Razorpay settlement by its settlement ID.",
    )
    def tool_fetch_settlement(
        key_id: str = Field(..., description="Razorpay API key ID"),
        key_secret: str = Field(..., description="Razorpay API key secret"),
        settlement_id: str = Field(..., description="Razorpay settlement ID (e.g. 'setl_XXXXXXXXXX')"),
    ) -> str:
        try:
            result = fetch_settlement(key_id, key_secret, settlement_id)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Failed fetch_settlement for '{settlement_id}': {e}")
            return json.dumps({"error": str(e)})
