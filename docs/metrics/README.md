# Metrics

Product KPIs and the PostHog event plan that feeds them.

## What goes here

- `kpis.md` — each KPI with its definition, formula, owner, target and the events it uses
- `events.md` — the tracking plan: one entry per event

| Event                | Trigger                         | Properties                     | Source story |
| -------------------- | ------------------------------- | ------------------------------ | ------------ |
| `tenant_signed_up`   | Tenant record created           | `plan`, `referrer`             | US-001       |

## What does not go here

- Infrastructure metrics and alerts → [operations/observability/](../operations/observability/README.md)
- Epic success metrics → the PRD, which references KPIs and events defined here

## Rules

- Event names are `object_action` in snake_case and past tense (`invoice_paid`). Properties are snake_case.
- An event is added here in the same PR that implements it. Removing an event requires checking which KPIs depend on it.
- No personal data in event properties beyond what [legal/privacy/](../legal/privacy/README.md) allows.
