# Integrations

Our contract with each third party (Resend, R2, payment gateways, inbound and outbound webhooks).

## What goes here

One file per provider covering:

- Purpose and the features we use
- Authentication and where its secrets are stored (the location, never the value)
- Limits: rate limits, quotas, payload sizes, costs
- Failure handling: timeouts, retries and backoff, idempotency keys, circuit breaking, what users see
- Webhooks: signature verification, replay protection, event ordering
- Sandbox and test accounts
- Links to the provider's documentation and status page

## What does not go here

- Why we chose the provider → [decisions/](../decisions/README.md)
- Account and cost inventory → [operations/infrastructure/](../operations/infrastructure/README.md)

## Naming

`<provider>.md`, e.g. `resend.md`, `cloudflare-r2.md`.
