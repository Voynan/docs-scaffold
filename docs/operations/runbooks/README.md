# Runbooks

Procedures someone can follow under pressure, without prior context.

## What goes here

One procedure per file, each with:

- **When to use:** the alert, symptom or request that triggers it
- **Prerequisites:** access, tools, approvals
- **Steps:** numbered, copy-pasteable commands, with the expected output of each
- **Verification:** how to confirm it worked
- **Rollback:** how to undo it if it did not
- **Last exercised:** the date the procedure was last run, in production or a drill

## What does not go here

- Secrets → the password manager; name the entry, never the value
- Explanations of how the system works → [architecture/](../../architecture/README.md)

## Rules

- Run each critical runbook (backup restore above all) at least once per quarter and update **Last exercised**. A procedure never run is a hypothesis.
- Every alert in [observability/](../observability/README.md) links to the runbook that handles it.

## Naming

`<verb>-<object>.md`, e.g. `deploy.md`, `rollback-release.md`, `restore-backup.md`, `rotate-secrets.md`.
