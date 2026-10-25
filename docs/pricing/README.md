# Pricing

What we sell and how we charge for it.

## What goes here

- `plans.md` — plans, prices, currencies and billing periods
- `limits.md` — quotas and feature flags per plan
- Billing rules: trials, proration, upgrade, downgrade, cancellation, refunds, dunning

## What does not go here

- Pricing strategy and research → [knowledge/](../knowledge/README.md)
- Payment gateway contract and failure handling → [integrations/](../integrations/README.md)

## Rules

- Billing rules the system enforces are business rules: give them a `BR-NNN` ID in [requirements/business-rules.md](../requirements/README.md) and reference that ID here instead of restating them.
- Record when each price or limit took effect, so support can explain what a customer was charged.

## Naming

Lowercase kebab-case, one topic per file.
