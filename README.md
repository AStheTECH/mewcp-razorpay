# CL Razorpay MCP Server

**Interact with Razorpay's payment infrastructure — orders, payments, refunds, and settlements — via API.**

A Model Context Protocol (MCP) server that exposes Razorpay's REST API for managing orders, capturing payments, processing refunds, and querying settlements.

---

## Overview

The CL Razorpay MCP Server provides stateless, multi-tenant access to the Razorpay API:

- **Order management** — create, fetch, update, and list orders
- **Payment operations** — fetch, capture, and update payments
- **Refund handling** — issue full or partial refunds, query refund status
- **Settlement queries** — list and inspect settlement records

Perfect for:

- Automating payment operations from AI agents or internal tools
- Querying transaction history and settlement data programmatically
- Building Claude-powered finance dashboards or customer support bots

---

## Authentication

This server is **stateless and multi-tenant**. Every tenant-facing tool accepts `key_id` and `key_secret` on each call. Credentials are never stored server-side.

Obtain your API keys from the [Razorpay Dashboard](https://dashboard.razorpay.com/app/keys):

1. Log in to your Razorpay Dashboard.
2. Navigate to **Settings → API Keys**.
3. Click **Generate Test Key** (for sandbox) or **Generate Live Key**.
4. Copy the **Key ID** and **Key Secret** — the secret is shown only once.

Use the test-mode keys against `https://api.razorpay.com/v1` — Razorpay's sandbox is live mode with test credentials, no separate base URL needed.

---

## Tools

<details>
<summary><code>health_check</code> — Verify server is running</summary>

Lightweight ping that confirms the MCP server is live. No auth required.

**Inputs:** none

**Output:**

```json
{ "status": "ok", "server": "CL Razorpay MCP Server" }
```

</details>

---

### Orders

<details>
<summary><code>create_order</code> — Create a new Razorpay order</summary>

Creates an order that is required before initiating a payment on the frontend SDK.

**Inputs:**

- `key_id` (string, required) — Razorpay API key ID
- `key_secret` (string, required) — Razorpay API key secret
- `amount` (integer, required) — Amount in smallest currency unit (e.g. paise for INR; ₹500 = `50000`)
- `currency` (string, required) — ISO 4217 currency code, e.g. `"INR"`
- `receipt` (string, optional) — Merchant receipt number (max 40 chars)
- `notes` (object, optional) — Key-value metadata to attach
- `partial_payment` (boolean, optional) — Whether partial payments are allowed (default: `false`)

**Output:**

```json
{
  "id": "order_XXXXXXXXXX",
  "entity": "order",
  "amount": 50000,
  "currency": "INR",
  "status": "created",
  "receipt": "receipt_001",
  "created_at": 1690000000
}
```

**Usage Example:**

```bash
POST /mcp/razorpay/create_order

{
  "key_id": "rzp_test_XXXXXXXX",
  "key_secret": "XXXXXXXXXXXXXXXX",
  "amount": 50000,
  "currency": "INR",
  "receipt": "receipt_001"
}
```

</details>

---

<details>
<summary><code>fetch_order</code> — Fetch a single order by ID</summary>

Retrieves full details of a specific order.

**Inputs:**

- `key_id` (string, required)
- `key_secret` (string, required)
- `order_id` (string, required) — e.g. `"order_XXXXXXXXXX"`

**Output:** Full order object as returned by Razorpay API.

</details>

---

<details>
<summary><code>fetch_all_orders</code> — List all orders with pagination</summary>

Retrieves a paginated list of orders, optionally filtered by creation timestamp.

**Inputs:**

- `key_id` (string, required)
- `key_secret` (string, required)
- `count` (integer, optional) — Number to return (default: `10`, max: `100`)
- `skip` (integer, optional) — Offset for pagination (default: `0`)
- `from_timestamp` (integer, optional) — Unix epoch; fetch orders created after this
- `to_timestamp` (integer, optional) — Unix epoch; fetch orders created before this

</details>

---

<details>
<summary><code>fetch_payments_for_order</code> — Fetch payments linked to an order</summary>

Retrieves all payment attempts made against a specific order ID.

**Inputs:**

- `key_id` (string, required)
- `key_secret` (string, required)
- `order_id` (string, required) — e.g. `"order_XXXXXXXXXX"`

</details>

---

<details>
<summary><code>update_order</code> — Update notes on an order</summary>

Updates the `notes` key-value map on an existing order.

**Inputs:**

- `key_id` (string, required)
- `key_secret` (string, required)
- `order_id` (string, required)
- `notes` (object, required) — Key-value pairs to set

</details>

---

### Payments

<details>
<summary><code>fetch_payment</code> — Fetch a single payment by ID</summary>

Retrieves details of a specific payment.

**Inputs:**

- `key_id` (string, required)
- `key_secret` (string, required)
- `payment_id` (string, required) — e.g. `"pay_XXXXXXXXXX"`

</details>

---

<details>
<summary><code>fetch_all_payments</code> — List all payments with pagination</summary>

Retrieves a paginated list of payments with optional timestamp filters.

**Inputs:**

- `key_id` (string, required)
- `key_secret` (string, required)
- `count` (integer, optional) — default `10`, max `100`
- `skip` (integer, optional) — default `0`
- `from_timestamp` (integer, optional)
- `to_timestamp` (integer, optional)

</details>

---

<details>
<summary><code>capture_payment</code> — Capture an authorized payment</summary>

Changes a payment from `authorized` to `captured`. Amount must exactly match the authorized amount.

**Inputs:**

- `key_id` (string, required)
- `key_secret` (string, required)
- `payment_id` (string, required) — e.g. `"pay_XXXXXXXXXX"`
- `amount` (integer, required) — Must match the authorized amount exactly
- `currency` (string, required) — e.g. `"INR"`

</details>

---

<details>
<summary><code>update_payment</code> — Update notes on a payment</summary>

Updates the `notes` key-value map on an existing payment.

**Inputs:**

- `key_id` (string, required)
- `key_secret` (string, required)
- `payment_id` (string, required)
- `notes` (object, required)

</details>

---

### Refunds

<details>
<summary><code>create_refund</code> — Issue a full or partial refund</summary>

Creates a refund for a captured payment. Omit `amount` for a full refund.

**Inputs:**

- `key_id` (string, required)
- `key_secret` (string, required)
- `payment_id` (string, required) — e.g. `"pay_XXXXXXXXXX"`
- `amount` (integer, optional) — Partial refund amount; omit for full refund
- `speed` (string, optional) — `"normal"` (default) or `"optimum"`
- `notes` (object, optional) — Key-value metadata
- `receipt` (string, optional) — Merchant receipt for the refund

**Output:**

```json
{
  "id": "rfnd_XXXXXXXXXX",
  "entity": "refund",
  "amount": 50000,
  "payment_id": "pay_XXXXXXXXXX",
  "speed_processed": "normal",
  "status": "processed"
}
```

</details>

---

<details>
<summary><code>fetch_refund</code> — Fetch a single refund by ID</summary>

**Inputs:**

- `key_id` (string, required)
- `key_secret` (string, required)
- `refund_id` (string, required) — e.g. `"rfnd_XXXXXXXXXX"`

</details>

---

<details>
<summary><code>fetch_all_refunds</code> — List all refunds with pagination</summary>

**Inputs:**

- `key_id` (string, required)
- `key_secret` (string, required)
- `count` (integer, optional) — default `10`, max `100`
- `skip` (integer, optional) — default `0`
- `from_timestamp` (integer, optional)
- `to_timestamp` (integer, optional)

</details>

---

<details>
<summary><code>fetch_refunds_for_payment</code> — Fetch refunds for a payment</summary>

**Inputs:**

- `key_id` (string, required)
- `key_secret` (string, required)
- `payment_id` (string, required) — e.g. `"pay_XXXXXXXXXX"`
- `count` (integer, optional) — default `10`
- `skip` (integer, optional) — default `0`

</details>

---

<details>
<summary><code>update_refund</code> — Update notes on a refund</summary>

**Inputs:**

- `key_id` (string, required)
- `key_secret` (string, required)
- `refund_id` (string, required)
- `notes` (object, required)

</details>

---

### Settlements

<details>
<summary><code>fetch_all_settlements</code> — List all settlements with pagination</summary>

**Inputs:**

- `key_id` (string, required)
- `key_secret` (string, required)
- `count` (integer, optional) — default `10`, max `100`
- `skip` (integer, optional) — default `0`
- `from_timestamp` (integer, optional)
- `to_timestamp` (integer, optional)

</details>

---

<details>
<summary><code>fetch_settlement</code> — Fetch a single settlement by ID</summary>

**Inputs:**

- `key_id` (string, required)
- `key_secret` (string, required)
- `settlement_id` (string, required) — e.g. `"setl_XXXXXXXXXX"`

</details>

---

<details>
<summary><strong>API Parameters Reference</strong></summary>

### Common Parameters

- `count` — Number of records to return (integer, 1–100, default 10)
- `skip` — Number of records to skip for pagination (integer, default 0)
- `from_timestamp` — Unix epoch integer; lower bound on `created_at`
- `to_timestamp` — Unix epoch integer; upper bound on `created_at`

### Resource ID Formats

**Order:**
```
order_{alphanumeric}
Example: order_OE1jIbY9HrFaXw
```

**Payment:**
```
pay_{alphanumeric}
Example: pay_OE1jIbY9HrFaXw
```

**Refund:**
```
rfnd_{alphanumeric}
Example: rfnd_OE1jIbY9HrFaXw
```

**Settlement:**
```
setl_{alphanumeric}
Example: setl_OE1jIbY9HrFaXw
```

</details>

---

<details>
<summary><strong>API Key Guide</strong></summary>

All tools require Razorpay API credentials. Here's how to obtain them:

### Step 1: Sign Up / Log In

1. Go to [Razorpay Dashboard](https://dashboard.razorpay.com/)
2. Sign up or log into your account

### Step 2: Generate API Keys

1. Navigate to **Settings → API Keys**
2. Click **Generate Test Key** for sandbox or **Regenerate Live Key** for production
3. Download or copy both **Key ID** and **Key Secret** immediately

### Step 3: Use Credentials Per Request

Pass `key_id` and `key_secret` in every tool call. The server uses HTTP Basic Auth (`key_id` as username, `key_secret` as password) on each request.

### Step 4: Required Permissions

Ensure your Razorpay account has:

- `payments:read` — Read payment details
- `payments:write` — Capture and update payments
- `orders:read` — Read order details
- `orders:write` — Create and update orders
- `refunds:read` — Read refund details
- `refunds:write` — Create and update refunds
- `settlements:read` — Read settlement details

Refer to the [Razorpay Authentication Guide](https://razorpay.com/docs/api/authentication/) for details.

</details>

---

<details>
<summary><strong>Troubleshooting</strong></summary>

### Missing or Invalid API Key

- **Cause:** `key_id` or `key_secret` is missing, incorrect, or belongs to a different mode (test vs live)
- **Solution:**
  1. Re-copy credentials from the Razorpay Dashboard
  2. Ensure you are using test keys for sandbox and live keys for production
  3. Regenerate keys if they have been rotated

### Insufficient Credits / Rate Limiting

- **Cause:** API calls have exceeded your account's rate limits
- **Solution:**
  1. Reduce request frequency
  2. Check [Razorpay API Best Practices](https://razorpay.com/docs/api/best-practices/) for rate limit guidance

### Malformed Request Payload

- **Cause:** Required fields missing or wrong types
- **Solution:**
  1. Ensure `amount` is an integer in smallest currency unit (paise, not rupees)
  2. Ensure all required tool parameters are provided
  3. Verify `currency` is a valid ISO 4217 code

### Payment Cannot Be Captured

- **Cause:** Payment is not in `authorized` state, or amount mismatch
- **Solution:**
  1. Check payment status with `fetch_payment` before capturing
  2. Ensure `amount` in `capture_payment` exactly matches the authorized amount

### Refund Cannot Be Created

- **Cause:** Payment is not in `captured` state, or has already been fully refunded
- **Solution:**
  1. Verify payment status with `fetch_payment`
  2. Check existing refunds with `fetch_refunds_for_payment`

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Razorpay API Documentation](https://razorpay.com/docs/api/)** — Official API reference
- **[Razorpay Authentication Guide](https://razorpay.com/docs/api/authentication/)** — Auth setup guide
- **[Razorpay Orders API](https://razorpay.com/docs/api/orders/)** — Orders endpoint reference
- **[Razorpay Payments API](https://razorpay.com/docs/api/payments/)** — Payments endpoint reference
- **[Razorpay Refunds API](https://razorpay.com/docs/api/refunds/)** — Refunds endpoint reference
- **[Razorpay Settlements API](https://razorpay.com/docs/api/settlements/)** — Settlements endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification

</details>

---

## Setup

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
# stdio (default — for local Claude Desktop / MCP clients)
python server.py

# SSE transport
python server.py --transport sse --host 127.0.0.1 --port 8001

# Streamable HTTP transport
python server.py --transport streamable-http --host 127.0.0.1 --port 8001
```

## Example Tool Call

```json
{
  "tool": "create_order",
  "arguments": {
    "key_id": "rzp_test_XXXXXXXX",
    "key_secret": "XXXXXXXXXXXXXXXX",
    "amount": 50000,
    "currency": "INR",
    "receipt": "receipt_001"
  }
}
```

## Project Structure

```text
cl-mcp-razorpay/
|-- server.py
|-- requirements.txt
|-- README.md
|-- .gitignore
`-- razorpay_mcp/
    |-- __init__.py
    |-- cli.py
    |-- config.py
    |-- schemas.py
    |-- service.py
    `-- tools.py
```
