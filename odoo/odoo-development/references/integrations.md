# Integrations and controllers

## Select an API for the target

JSON-2 was introduced in 19.0. It uses `POST /json/2/<model>/<method>` with a JSON object of named arguments, bearer API-key authorization, optional `X-Odoo-Database`, and optional `ids`/`context`. Database `/doc` describes available models/methods. Access uses the user's permissions. Each request is its own transaction: use one server method for an atomic business operation. Documentation restricts external API access to Custom plans; verify current entitlement. Keep keys secret and use a dedicated least-privilege integration user.

Source: [JSON-2 API](https://www.odoo.com/documentation/20.0/developer/reference/external_api.html).

Illustrative read-only request; obtain values from secure configuration and never print the key:

```python
import requests

response = requests.post(
    f"{base_url}/json/2/res.partner/search_read",
    headers={"Authorization": f"bearer {api_key}"},
    json={"domain": [["is_company", "=", True]], "fields": ["name"], "limit": 20},
    timeout=30,
)
response.raise_for_status()
partners = response.json()
```

This is an HTTP client illustration, not an installed executable or a guarantee about a particular database's schema.

Legacy XML-RPC/JSON-RPC use services and `execute_kw` positional/keyword conventions. The researched 20.0 notice says the **database service was removed in 20.0 / Online 19.1**, while common/object services are scheduled for removal in **22 / Online 21.1**. Recheck the notice before planning migrations. Custom `@route(type='jsonrpc')` controllers are outside that endpoint deprecation. Do not claim every RPC mechanism disappears together.

Source: [legacy external RPC](https://www.odoo.com/documentation/20.0/developer/reference/external_rpc_api.html).

Recommended integration design: establish stable external IDs, pagination and reconciliation rules; validate payloads; use timeouts; classify transient/permanent failures; make writes idempotent before retrying uncertain requests; log correlation IDs and outcomes without credentials or unnecessary personal data. An HTTP timeout does not prove the remote transaction rolled back.

## Controllers

Choose `http` versus the version's JSON route type, explicit methods, auth, CORS and CSRF behavior. Current `http` routes default to CSRF protection and `jsonrpc` routes do not. Current bearer routes require an appropriate `bearer_scope`; missing authorization can fall back to a user session, so enforce API-only intent explicitly when required. Re-decorate overridden controller methods with `@route()` to keep routes published. Validate record ownership and allowed inputs before privileged work. Avoid caller-controlled model/method dispatch. Use framework response helpers.

Source: [web controllers](https://www.odoo.com/documentation/20.0/developer/reference/backend/http.html).

## Incoming/outgoing automation

Treat webhook URLs, signing secrets and payloads as sensitive. Map event data to approved actions explicitly. Recommended checks include authentication/signature, duplicate and replay handling, timestamp tolerance, wrong-company records and provider retries. Keep browser-facing endpoints and machine integrations distinct where their contracts differ.

Sources: [Studio webhooks](https://www.odoo.com/documentation/20.0/applications/studio/automated_actions/webhooks.html), [automation rules](https://www.odoo.com/documentation/20.0/applications/studio/automated_actions.html).

For payments, extend the documented provider/transaction/token methods and test through sandbox callbacks and reconciliation; do not mark transactions paid from a browser success redirect. For device/IoT work, inspect the target device/driver interface and test disconnection/reconnect behavior. For OCR/extraction, verify the current Extract API flow, version, callback or polling contract and billing before implementing calls.

Sources: [payment transaction](https://www.odoo.com/documentation/20.0/developer/reference/standard_modules/payment/payment_transaction.html), [device integration](https://www.odoo.com/documentation/20.0/developer/howtos/connect_device.html), [Extract API](https://www.odoo.com/documentation/20.0/developer/reference/extract_api.html).
