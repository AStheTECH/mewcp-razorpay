**Automate Razorpay payments, refunds, and settlements through AI.**

A Model Context Protocol (MCP) server that exposes Razorpay's API for managing orders, payments, refunds, and settlements.


## Overview

The Razorpay MCP Server provides full lifecycle payment management through AI:

- Create and track orders, capture and update payments
- Issue full or partial refunds with speed control
- Query settlements and reconcile transaction history

Perfect for:

- Automating refund workflows and customer support payment queries
- Building AI-powered dashboards that pull live payment and settlement data
- Triggering order creation and payment capture from conversational interfaces


## Tools

<details>
<summary><code>health_check</code> — Check server readiness</summary>

Returns a status object confirming the server is running and reachable.

**Inputs:** _(none)_

**Output:**

```json
{
  "status": "ok",
  "server": "CL Razorpay MCP Server"
}
```

</details>


<details>
<summary><code>create_order</code> — Create a new Razorpay order</summary>

Creates a new order object. The returned order ID is passed to the Razorpay checkout SDK on the frontend to initiate payment.

**Inputs:**
```
- `amount`          (integer, required) — Amount in smallest currency unit (e.g. paise for INR)
- `currency`        (string, required)  — ISO 4217 currency code, e.g. 'INR'
- `receipt`         (string, optional)  — Merchant receipt number (max 40 chars)
- `notes`           (object, optional)  — Key-value notes to attach to the order
- `partial_payment` (boolean, optional) — Whether partial payments are allowed (default: false)
```

**Output:**

```json
{
  "id": "order_XXXXXXXXXX",
  "entity": "order",
  "amount": 50000,
  "currency": "INR",
  "status": "created"
}
```

</details>


<details>
<summary><code>fetch_order</code> — Fetch a specific order</summary>

Retrieves full details of a single Razorpay order by its order ID.

**Inputs:**
```
- `order_id` (string, required) — Razorpay order ID (e.g. 'order_XXXXXXXXXX')
```

**Output:**

```json
{
  "id": "order_XXXXXXXXXX",
  "entity": "order",
  "amount": 50000,
  "amount_paid": 0,
  "status": "created"
}
```

</details>


<details>
<summary><code>fetch_all_orders</code> — Fetch paginated list of orders</summary>

Returns a filtered, paginated list of all Razorpay orders. Supports Unix timestamp range filtering.

**Inputs:**
```
- `count`          (integer, optional) — Number of orders to fetch, max 100 (default: 10)
- `skip`           (integer, optional) — Number of orders to skip for pagination (default: 0)
- `from_timestamp` (integer, optional) — Unix timestamp — fetch orders created after this time
- `to_timestamp`   (integer, optional) — Unix timestamp — fetch orders created before this time
```

**Output:**

```json
{
  "entity": "collection",
  "count": 10,
  "items": [...]
}
```

</details>


<details>
<summary><code>fetch_payments_for_order</code> — Fetch payments for a specific order</summary>

Returns all payments made against a given order ID.

**Inputs:**
```
- `order_id` (string, required) — Razorpay order ID (e.g. 'order_XXXXXXXXXX')
```

**Output:**

```json
{
  "entity": "collection",
  "count": 1,
  "items": [...]
}
```

</details>


<details>
<summary><code>update_order</code> — Update notes on an order</summary>

Patches the notes field on an existing order. Only the notes field can be updated after creation.

**Inputs:**
```
- `order_id` (string, required) — Razorpay order ID (e.g. 'order_XXXXXXXXXX')
- `notes`    (object, required) — Key-value notes to update on the order
```

**Output:**

```json
{
  "id": "order_XXXXXXXXXX",
  "notes": { "key": "value" }
}
```

</details>


<details>
<summary><code>fetch_payment</code> — Fetch a specific payment</summary>

Retrieves full details of a single Razorpay payment by its payment ID.

**Inputs:**
```
- `payment_id` (string, required) — Razorpay payment ID (e.g. 'pay_XXXXXXXXXX')
```

**Output:**

```json
{
  "id": "pay_XXXXXXXXXX",
  "entity": "payment",
  "amount": 50000,
  "currency": "INR",
  "status": "captured"
}
```

</details>


<details>
<summary><code>fetch_all_payments</code> — Fetch paginated list of payments</summary>

Returns a filtered, paginated list of all Razorpay payments. Supports Unix timestamp range filtering.

**Inputs:**
```
- `count`          (integer, optional) — Number of payments to fetch, max 100 (default: 10)
- `skip`           (integer, optional) — Number of payments to skip for pagination (default: 0)
- `from_timestamp` (integer, optional) — Unix timestamp — fetch payments created after this time
- `to_timestamp`   (integer, optional) — Unix timestamp — fetch payments created before this time
```

**Output:**

```json
{
  "entity": "collection",
  "count": 10,
  "items": [...]
}
```

</details>


<details>
<summary><code>capture_payment</code> — Capture an authorized payment</summary>

Captures a payment that is in `authorized` state. The amount must exactly match the authorized amount.

**Inputs:**
```
- `payment_id` (string, required)  — Razorpay payment ID (e.g. 'pay_XXXXXXXXXX')
- `amount`     (integer, required) — Amount to capture in smallest currency unit (must match authorized amount)
- `currency`   (string, required)  — ISO 4217 currency code, e.g. 'INR'
```

**Output:**

```json
{
  "id": "pay_XXXXXXXXXX",
  "status": "captured",
  "amount": 50000
}
```

</details>


<details>
<summary><code>update_payment</code> — Update notes on a payment</summary>

Patches the notes field on an existing payment.

**Inputs:**
```
- `payment_id` (string, required) — Razorpay payment ID (e.g. 'pay_XXXXXXXXXX')
- `notes`      (object, required) — Key-value notes to update on the payment
```

**Output:**

```json
{
  "id": "pay_XXXXXXXXXX",
  "notes": { "key": "value" }
}
```

</details>


<details>
<summary><code>create_refund</code> — Create a refund for a payment</summary>

Issues a full or partial refund for a captured payment. Omit amount for a full refund. Speed `optimum` uses instant refund where available.

**Inputs:**
```
- `payment_id` (string, required)  — Razorpay payment ID to refund (e.g. 'pay_XXXXXXXXXX')
- `amount`     (integer, optional) — Refund amount in smallest currency unit; omit for full refund
- `speed`      (string, optional)  — Refund speed: 'normal' (default) or 'optimum'
- `notes`      (object, optional)  — Key-value notes to attach to the refund
- `receipt`    (string, optional)  — Unique merchant receipt number for the refund
```

**Output:**

```json
{
  "id": "rfnd_XXXXXXXXXX",
  "entity": "refund",
  "amount": 50000,
  "speed_processed": "normal",
  "status": "processed"
}
```

</details>


<details>
<summary><code>fetch_refund</code> — Fetch a specific refund</summary>

Retrieves full details of a single Razorpay refund by its refund ID.

**Inputs:**
```
- `refund_id` (string, required) — Razorpay refund ID (e.g. 'rfnd_XXXXXXXXXX')
```

**Output:**

```json
{
  "id": "rfnd_XXXXXXXXXX",
  "entity": "refund",
  "amount": 50000,
  "status": "processed"
}
```

</details>


<details>
<summary><code>fetch_all_refunds</code> — Fetch paginated list of refunds</summary>

Returns a filtered, paginated list of all Razorpay refunds. Supports Unix timestamp range filtering.

**Inputs:**
```
- `count`          (integer, optional) — Number of refunds to fetch, max 100 (default: 10)
- `skip`           (integer, optional) — Number of refunds to skip for pagination (default: 0)
- `from_timestamp` (integer, optional) — Unix timestamp — fetch refunds created after this time
- `to_timestamp`   (integer, optional) — Unix timestamp — fetch refunds created before this time
```

**Output:**

```json
{
  "entity": "collection",
  "count": 10,
  "items": [...]
}
```

</details>


<details>
<summary><code>fetch_refunds_for_payment</code> — Fetch all refunds for a payment</summary>

Returns all refunds issued against a specific payment ID, with pagination support.

**Inputs:**
```
- `payment_id` (string, required)  — Razorpay payment ID (e.g. 'pay_XXXXXXXXXX')
- `count`      (integer, optional) — Number of refunds to fetch, max 100 (default: 10)
- `skip`       (integer, optional) — Number of refunds to skip for pagination (default: 0)
```

**Output:**

```json
{
  "entity": "collection",
  "count": 2,
  "items": [...]
}
```

</details>


<details>
<summary><code>update_refund</code> — Update notes on a refund</summary>

Patches the notes field on an existing refund.

**Inputs:**
```
- `refund_id` (string, required) — Razorpay refund ID (e.g. 'rfnd_XXXXXXXXXX')
- `notes`     (object, required) — Key-value notes to update on the refund
```

**Output:**

```json
{
  "id": "rfnd_XXXXXXXXXX",
  "notes": { "key": "value" }
}
```

</details>


<details>
<summary><code>fetch_all_settlements</code> — Fetch paginated list of settlements</summary>

Returns a filtered, paginated list of all Razorpay settlements. Supports Unix timestamp range filtering.

**Inputs:**
```
- `count`          (integer, optional) — Number of settlements to fetch, max 100 (default: 10)
- `skip`           (integer, optional) — Number of settlements to skip for pagination (default: 0)
- `from_timestamp` (integer, optional) — Unix timestamp — fetch settlements created after this time
- `to_timestamp`   (integer, optional) — Unix timestamp — fetch settlements created before this time
```

**Output:**

```json
{
  "entity": "collection",
  "count": 10,
  "items": [...]
}
```

</details>


<details>
<summary><code>fetch_settlement</code> — Fetch a specific settlement</summary>

Retrieves full details of a single Razorpay settlement by its settlement ID.

**Inputs:**
```
- `settlement_id` (string, required) — Razorpay settlement ID (e.g. 'setl_XXXXXXXXXX')
```

**Output:**

```json
{
  "id": "setl_XXXXXXXXXX",
  "entity": "settlement",
  "amount": 1000000,
  "status": "processed"
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Common Parameters</strong></summary>

- `count` — Number of records to return per request (max 100, default 10)
- `skip` — Number of records to skip; use with `count` for pagination
- `from_timestamp` — Unix epoch timestamp (seconds); filters records created at or after this time
- `to_timestamp` — Unix epoch timestamp (seconds); filters records created at or before this time

</details>

<details>
<summary><strong>Resource ID Formats</strong></summary>

**Orders:**

```
order_{alphanumeric}
Example: order_OGN1lSF2fk1JNW
```

**Payments:**

```
pay_{alphanumeric}
Example: pay_OGN1lSF2fk1JNW
```

**Refunds:**

```
rfnd_{alphanumeric}
Example: rfnd_OGN1lSF2fk1JNW
```

**Settlements:**

```
setl_{alphanumeric}
Example: setl_OGN1lSF2fk1JNW
```

</details>

<details>
<summary><strong>Amount Formatting</strong></summary>

All amounts are in the **smallest currency unit**:

- INR → paise (₹500.00 = `50000`)
- USD → cents ($10.00 = `1000`)
- EUR → cents (€10.00 = `1000`)

</details>


## Getting Your Razorpay API Keys

<details>
<summary><strong>Steps</strong></summary>

1. Go to the [Razorpay Dashboard](https://dashboard.razorpay.com/)
2. Navigate to **Settings** → **API Keys**
3. Click **Generate Test Key** (for test mode) or **Generate Live Key** (for production)
4. Copy the **Key ID** and **Key Secret** — the secret is only shown once; store it securely

> Use test mode keys (prefixed `rzp_test_`) during development and live keys (`rzp_live_`) in production.

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** API key not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_API_KEY` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check API key is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Razorpay credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Add your Razorpay Key ID and Key Secret
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check that `amount` is an integer in the smallest currency unit, not a decimal

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Razorpay API Error</strong></summary>

- **Cause:** Upstream Razorpay API returned an error
- **Solution:**
  1. Check Razorpay service status at [Razorpay Status Page](https://status.razorpay.com/)
  2. Verify your API keys have the required permissions for the operation
  3. Review the error message for specific details (e.g. payment not in `authorized` state for capture)

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Razorpay API Documentation](https://razorpay.com/docs/api/)** — Official API reference
- **[Razorpay Dashboard](https://dashboard.razorpay.com/)** — Manage keys, orders, and settlements
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling

</details>
