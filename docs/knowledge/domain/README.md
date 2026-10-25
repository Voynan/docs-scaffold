# Domain

How the client's business works, in the client's words.

## What goes here

- `glossary.md` — the ubiquitous language: one definition per term, used verbatim in code, UI and documents
- Descriptions of the client's processes and policies
- Summaries of applicable legislation, with links to the official text

## What does not go here

- Business rules the system enforces → [requirements/business-rules.md](../../requirements/README.md); they cite the document here as their source
- Personal data inventory and legal bases → [legal/privacy/](../../legal/privacy/README.md)

## Naming

Lowercase kebab-case, one topic per file. When a term in `glossary.md` changes, rename it in code and documents in the same PR.
