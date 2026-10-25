# API

What a client needs to know to use the API, beyond what the generated OpenAPI spec says.

## What goes here

- Overview: base URLs, environments, resource model
- Authentication and authorization
- Versioning and deprecation policy
- Pagination, filtering, errors, idempotency and rate limits
- End-to-end examples of common tasks

## What does not go here

- Endpoint-by-endpoint reference → the generated OpenAPI spec. Link to it; do not copy it.
- Third-party APIs we consume → [integrations/](../integrations/README.md)

## Naming

Lowercase kebab-case, one topic per file, e.g. `authentication.md`, `versioning.md`.
