# Architecture

How the system is built today. ADRs explain why each part changed; this folder describes the result, so nobody has to replay every ADR to understand the present.

## What goes here

- `overview.md` — the architecture description, following a lightweight arc42: goals and constraints, context, building blocks, runtime, deployment, cross-cutting concepts, risks and technical debt
- [diagrams/](diagrams/README.md) — one diagram per file, linked from `overview.md`, ADRs and other documents

## What does not go here

- The reasoning behind each choice → [decisions/](../decisions/README.md); `overview.md` links to the ADR instead of repeating it
- Data model → [data/](../data/README.md)
- Screen flows → [design/](../design/README.md)
- Service inventory and costs → [operations/infrastructure/](../operations/infrastructure/README.md)

## Rules

- When an ADR is accepted, update `overview.md` and the affected diagrams in the same PR.
- `overview.md` explains; diagrams show. Keep explanations out of diagram files and diagrams out of `overview.md`.

## Template

[architecture-overview.md](../_templates/architecture-overview.md)
