# Diagrams

Diagrams as code in Mermaid, one per file, rendered by GitHub.

## What goes here

- C4 diagrams: system context and containers, components where useful
- Sequence diagrams of critical flows (signup, billing, webhooks)
- State and flow diagrams of core domain entities

## What does not go here

- The explanation of what a diagram shows → `architecture/overview.md`, the ADR or the document that links to it
- Screen flows and wireframes → [design/](../../design/README.md)
- Entity-relationship model → [data/](../../data/README.md)
- Images exported from other tools. If one is unavoidable, commit its source next to it.

## Rules

- One diagram per file. A file holds a title, a one-line caption, the date it was last checked against the system, and the Mermaid block.
- A diagram that disagrees with the system is a defect. Update it in the same PR as the change.
- CI renders every diagram; a syntax error fails the build.

## Naming

`<kind>-<subject>.md`, where kind is `c4-context`, `c4-container`, `c4-component`, `sequence`, `state` or `flow`. Examples: `c4-container-platform.md`, `sequence-checkout.md`, `state-invoice.md`.

## Template

[diagram.md](../../_templates/diagram.md)
