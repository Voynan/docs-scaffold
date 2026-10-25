---
paths:
  - "docs/**"
---

# Documentation standard

[`docs/README.md`](../../docs/README.md) is the source of truth for the docs standard; read it before creating or changing anything under `docs/`.

## Where things are

- **Rules, ID conventions, Definitions of Ready and Done:** `docs/README.md`
- **What belongs in each folder and how files are named:** that folder's `README.md`
- **Templates for new documents:** `docs/_templates/`. Copy one, never start from a blank file.
- **Personal notes:** `docs/dev/` is not versioned. Do not put project knowledge there or read it as project truth.

## When changing docs

- Cite the upstream artifacts by ID in the front matter; never maintain downstream lists by hand.
- Next ID = highest existing ID + 1. Never reuse or renumber IDs, including acceptance criteria.
- `<!-- author-stamp: ... -->` lines are written by hooks around Edit and Write. Never write or edit them by hand; for changes made through shell commands, use the `author-stamp` skill.

## Before reporting work as done

```sh
python tools/trace-check/trace_check.py --tests <test folders>
npx markdownlint-cli2
```

Fix every error. The traceability matrix is generated; never commit it.
