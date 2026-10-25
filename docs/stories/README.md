# Stories

User stories with acceptance criteria written in EARS. Each story is the unit of delivery and of verification.

## What goes here

- One file per story, citing its PRD and any NFR, BR or ADR it must respect
- Acceptance criteria with stable IDs (`US-001.AC1`), each referenced by at least one test

## What does not go here

- Workflow status, estimates, assignees → the `[US-001] ...` issue in GitHub Projects
- Rules that apply to several stories → [requirements/](../requirements/README.md); cite them by ID
- Implementation notes → code comments, ADRs or the PR description

## Rules

- Acceptance criteria are never renumbered. Removing one leaves a gap.
- A story that is abandoned is deleted; its ID is not reused.

## Naming

`US-NNN-slug.md`, e.g. `US-001-tenant-signup.md`.

## Template

[story.md](../_templates/story.md)
