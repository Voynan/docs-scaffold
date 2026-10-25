# Decisions

Architecture Decision Records: one significant decision per file, with its context and consequences.

## What goes here

A decision is significant when it is costly to reverse or constrains future work: structure, technology, data model, integration pattern, security model.

## What does not go here

- The current architecture as a whole → [architecture/](../architecture/README.md)
- Product decisions → the PRD
- Reversible, local choices → code review and the PR description

## Rules

- An ADR starts as `proposed` and is reviewed in a PR. Merging marks it `accepted` or `rejected`.
- Accepted ADRs are not edited, except to change their status. To change a decision, write a new ADR with `supersedes:` and set `superseded_by:` on the old one.
- Cite the drivers by ID (NFR, BR, PRD, research note).

## Naming

`ADR-NNNN-slug.md`, e.g. `ADR-0001-schema-per-tenant.md`.

## Template

[adr.md](../_templates/adr.md)
